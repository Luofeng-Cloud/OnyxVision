import os
import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.database import get_db
from app.models import ScanDirectoryRequest
from app.scraper.matcher import FilenameMatcher, TMDBScraper

router = APIRouter(prefix="/api/media", tags=["Media"])

def format_media_row(row: Dict[str, Any], conn=None) -> Dict[str, Any]:
    """Helper to convert a media_items DB row into a rich OnyxVision media JSON object."""
    item = dict(row)
    
    # Parse JSON fields safely
    for f in ("genres", "actors", "directors", "tags"):
        val = item.get(f)
        if isinstance(val, str):
            try:
                item[f] = json.loads(val)
            except Exception:
                item[f] = []
        elif val is None:
            item[f] = []

    # Parse technical_info
    tech = item.get("technical_info")
    if isinstance(tech, str):
        try:
            item["technical_info"] = json.loads(tech)
        except Exception:
            item["technical_info"] = {}
    elif tech is None:
        item["technical_info"] = {}

    # Attach stream proxy route if item has a stream_url or local_path
    item["playback_url"] = f"/api/stream/{item['id']}"

    # Map human-readable source label
    if not item.get("source"):
        sid = str(item.get("source_id") or "")
        if "emby" in sid:
            item["source"] = "Emby"
        elif "jellyfin" in sid:
            item["source"] = "Jellyfin"
        elif "webdav" in sid:
            item["source"] = "WebDAV"
        elif "local" in sid:
            item["source"] = "本地"
        else:
            item["source"] = "Emby"

    # Fetch playback history if connection is provided
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT position_seconds, duration_seconds, playback_percentage, is_played, last_played_at
        FROM playback_history WHERE item_id = ?
        """, (item["id"],))
        ph = cursor.fetchone()
        if ph:
            item["playback"] = {
                "position_seconds": ph["position_seconds"],
                "duration_seconds": ph["duration_seconds"],
                "playback_percentage": round(ph["playback_percentage"], 1),
                "is_played": bool(ph["is_played"]),
                "last_played_at": ph["last_played_at"]
            }
            item["progress"] = round(ph["playback_percentage"] / 100.0, 3)
            item["playback_percentage"] = round(ph["playback_percentage"], 1)
        else:
            item["playback"] = {
                "position_seconds": 0.0,
                "duration_seconds": float(item.get("duration", 0)),
                "playback_percentage": 0.0,
                "is_played": False,
                "last_played_at": None
            }
            item["progress"] = 0.0
            item["playback_percentage"] = 0.0

    return item


@router.get("/home")
def get_home_feed(source_id: Optional[str] = Query(None, description="Optional source ID filter")):
    """
    Returns aggregated home page feed:
    - hero_banners: Top 6 curated items with high-res backdrop, logo, ambient color & badges
    - continue_watching: In-progress items from playback_history
    - latest_added: Recently imported movies & series
    - movies: Curated top movies
    - tv_shows: Curated top TV series
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # If no sources exist in DB or specified source has no items, return empty cleanly
        if source_id:
            cursor.execute("SELECT id FROM sources WHERE id = ?", (source_id,))
            if not cursor.fetchone():
                return {
                    "hero_banners": [],
                    "continue_watching": [],
                    "latest_added": [],
                    "movies": [],
                    "tv_shows": []
                }
        else:
            cursor.execute("SELECT count(*) FROM sources")
            if cursor.fetchone()[0] == 0:
                return {
                    "hero_banners": [],
                    "continue_watching": [],
                    "latest_added": [],
                    "movies": [],
                    "tv_shows": []
                }

        # 1. Hero Banners: High-rated items with backdrops
        if source_id:
            cursor.execute("""
            SELECT * FROM media_items
            WHERE source_id = ? AND type IN ('movie', 'series') AND backdrop != ''
            ORDER BY is_favorite DESC, rating DESC
            LIMIT 6
            """, (source_id,))
        else:
            cursor.execute("""
            SELECT * FROM media_items
            WHERE type IN ('movie', 'series') AND backdrop != ''
            ORDER BY is_favorite DESC, rating DESC
            LIMIT 6
            """)
        hero_banners = [format_media_row(r, conn) for r in cursor.fetchall()]

        # 2. Continue Watching: In-progress playback (0 < % < 95)
        if source_id:
            cursor.execute("""
            SELECT m.*, p.position_seconds, p.duration_seconds, p.playback_percentage, p.last_played_at
            FROM playback_history p
            JOIN media_items m ON p.item_id = m.id
            WHERE m.source_id = ? AND p.is_played = 0 AND p.playback_percentage > 0 AND p.playback_percentage < 95
            ORDER BY p.last_played_at DESC
            LIMIT 10
            """, (source_id,))
        else:
            cursor.execute("""
            SELECT m.*, p.position_seconds, p.duration_seconds, p.playback_percentage, p.last_played_at
            FROM playback_history p
            JOIN media_items m ON p.item_id = m.id
            WHERE p.is_played = 0 AND p.playback_percentage > 0 AND p.playback_percentage < 95
            ORDER BY p.last_played_at DESC
            LIMIT 10
            """)
        continue_watching = []
        for r in cursor.fetchall():
            row_dict = dict(r)
            item = format_media_row(row_dict, conn)
            if item.get("type") == "episode" and item.get("series_id"):
                cursor.execute("SELECT title FROM media_items WHERE id = ?", (item["series_id"],))
                s_row = cursor.fetchone()
                if s_row:
                    item["series_title"] = s_row["title"]
            continue_watching.append(item)

        # 3. Latest Added
        if source_id:
            cursor.execute("""
            SELECT * FROM media_items
            WHERE source_id = ? AND type IN ('movie', 'series')
            ORDER BY created_at DESC
            LIMIT 12
            """, (source_id,))
        else:
            cursor.execute("""
            SELECT * FROM media_items
            WHERE type IN ('movie', 'series')
            ORDER BY created_at DESC
            LIMIT 12
            """)
        latest_added = [format_media_row(r, conn) for r in cursor.fetchall()]

        # 4. Movies Shelf
        if source_id:
            cursor.execute("""
            SELECT * FROM media_items
            WHERE source_id = ? AND type = 'movie'
            ORDER BY rating DESC, created_at DESC
            LIMIT 15
            """, (source_id,))
        else:
            cursor.execute("""
            SELECT * FROM media_items
            WHERE type = 'movie'
            ORDER BY rating DESC, created_at DESC
            LIMIT 15
            """)
        movies = [format_media_row(r, conn) for r in cursor.fetchall()]

        # 5. TV Shows Shelf
        if source_id:
            cursor.execute("""
            SELECT * FROM media_items
            WHERE source_id = ? AND type = 'series'
            ORDER BY rating DESC, created_at DESC
            LIMIT 15
            """, (source_id,))
        else:
            cursor.execute("""
            SELECT * FROM media_items
            WHERE type = 'series'
            ORDER BY rating DESC, created_at DESC
            LIMIT 15
            """)
        tv_shows = [format_media_row(r, conn) for r in cursor.fetchall()]

        return {
            "hero_banners": hero_banners,
            "continue_watching": continue_watching,
            "latest_added": latest_added,
            "movies": movies,
            "tv_shows": tv_shows
        }


@router.get("/items")
def get_media_items(
    type: Optional[str] = Query(None, description="Filter by type: movie, series, episode"),
    source_id: Optional[str] = Query(None, description="Filter by source ID"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    search: Optional[str] = Query(None, description="Search keyword in title, overview"),
    sort_by: str = Query("created_at", description="Sort by: rating, year, created_at, title"),
    order: str = Query("desc", description="Sort order: asc, desc"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Search and filter media items with pagination.
    """
    valid_sort = {
        "rating": "rating",
        "year": "year",
        "created_at": "created_at",
        "title": "title"
    }
    sort_col = valid_sort.get(sort_by, "created_at")
    sort_direction = "ASC" if order.lower() == "asc" else "DESC"

    query_parts = ["1=1"]
    params = []

    if type:
        query_parts.append("type = ?")
        params.append(type)
    else:
        # Default don't show standalone episodes in library browse view unless requested
        query_parts.append("type IN ('movie', 'series')")

    if source_id:
        query_parts.append("source_id = ?")
        params.append(source_id)

    if genre:
        query_parts.append("genres LIKE ?")
        params.append(f"%{genre}%")

    if search:
        query_parts.append("(title LIKE ? OR original_title LIKE ? OR overview LIKE ?)")
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])

    where_clause = " AND ".join(query_parts)

    with get_db() as conn:
        cursor = conn.cursor()

        # Get total count
        cursor.execute(f"SELECT COUNT(*) FROM media_items WHERE {where_clause}", params)
        total = cursor.fetchone()[0]

        # Get page items
        sql = f"""
        SELECT * FROM media_items
        WHERE {where_clause}
        ORDER BY {sort_col} {sort_direction}
        LIMIT ? OFFSET ?
        """
        cursor.execute(sql, params + [limit, offset])
        items = [format_media_row(r, conn) for r in cursor.fetchall()]

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": items
        }


@router.get("/genres")
def get_genres(source_id: Optional[str] = Query(None, description="Filter genres by source ID")):
    """
    Returns distinct list of genres available across media items.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        if source_id:
            cursor.execute("SELECT genres FROM media_items WHERE source_id = ? AND genres IS NOT NULL AND genres != ''", (source_id,))
        else:
            cursor.execute("SELECT genres FROM media_items WHERE genres IS NOT NULL AND genres != ''")
        
        all_genres = set()
        for row in cursor.fetchall():
            val = row["genres"]
            if isinstance(val, str):
                try:
                    g_list = json.loads(val)
                    if isinstance(g_list, list):
                        for g in g_list:
                            if g:
                                all_genres.add(str(g).strip())
                except Exception:
                    for g in val.split(","):
                        if g.strip():
                            all_genres.add(g.strip())
            elif isinstance(val, list):
                for g in val:
                    if g:
                        all_genres.add(str(g).strip())

        return {"genres": sorted(list(all_genres))}


@router.get("/{item_id}")
def get_media_detail(item_id: str):
    """
    Fetches full media item detail.
    For TV series, automatically groups and embeds all episodes by season.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM media_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")

        item = format_media_row(row, conn)

        # If it's a TV series, retrieve all associated episodes
        if item.get("type") == "series":
            cursor.execute("""
            SELECT * FROM media_items
            WHERE series_id = ? AND type = 'episode'
            ORDER BY season_number ASC, episode_number ASC
            """, (item_id,))
            ep_rows = cursor.fetchall()
            
            seasons_map = {}
            for ep_r in ep_rows:
                ep_item = format_media_row(ep_r, conn)
                s_num = ep_item.get("season_number", 1)
                if s_num not in seasons_map:
                    seasons_map[s_num] = {
                        "season_number": s_num,
                        "name": f"第 {s_num} 季",
                        "episodes": []
                    }
                seasons_map[s_num]["episodes"].append(ep_item)

            item["seasons"] = list(seasons_map.values())

        # If it's an episode, fetch parent series title
        elif item.get("type") == "episode" and item.get("series_id"):
            cursor.execute("SELECT title FROM media_items WHERE id = ?", (item["series_id"],))
            series_row = cursor.fetchone()
            if series_row:
                item["series_title"] = series_row["title"]

        return item


@router.post("/{item_id}/favorite")
def toggle_favorite(item_id: str):
    """Toggles the favorite state of a media item."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_favorite FROM media_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")

        new_val = 0 if row["is_favorite"] else 1
        cursor.execute("UPDATE media_items SET is_favorite = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_val, item_id))
        return {"success": True, "is_favorite": bool(new_val)}


@router.get("/genres/list")
def list_genres():
    """Returns list of distinct genres across all media items."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT genres FROM media_items WHERE type IN ('movie', 'series')")
        genre_set = set()
        for row in cursor.fetchall():
            try:
                g_list = json.loads(row["genres"])
                for g in g_list:
                    if g:
                        genre_set.add(g)
            except Exception:
                pass
        return {"genres": sorted(list(genre_set))}


@router.post("/scan-directory")
async def scan_local_directory(req: ScanDirectoryRequest):
    """
    Recursively scans a local directory, parses filenames via FilenameMatcher,
    enriches with TMDBScraper, and saves into media_items.
    """
    target_dir = Path(req.directory_path)
    if not target_dir.exists() or not target_dir.is_dir():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Directory does not exist or is not a folder.")

    source_id = req.source_id or "source_demo_local"
    supported_exts = {".mp4", ".mkv", ".avi", ".ts", ".m2ts", ".mov", ".wmv", ".flv"}
    found_files = []

    for root, _, files in os.walk(target_dir):
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in supported_exts:
                found_files.append(Path(root) / f)

    scraper = TMDBScraper()
    imported_count = 0

    with get_db() as conn:
        cursor = conn.cursor()
        for fpath in found_files:
            parsed = FilenameMatcher.clean(fpath.name)
            enriched = await scraper.enrich_item(parsed)

            item_id = f"local_{uuid.uuid5(uuid.NAMESPACE_URL, str(fpath)).hex[:12]}"
            item_type = "episode" if enriched.get("is_tv") else "movie"

            cursor.execute("""
            INSERT OR REPLACE INTO media_items (
                id, source_id, type, title, original_title, year, overview,
                poster, backdrop, rating, ambient_color, tags,
                technical_info, local_path, season_number, episode_number
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id, source_id, item_type, enriched["title"], enriched.get("original_title", enriched["title"]),
                enriched.get("year"), enriched.get("overview", ""), enriched.get("poster", ""), enriched.get("backdrop", ""),
                enriched.get("rating", 8.0), enriched.get("ambient_color", "#1e293b"),
                json.dumps(enriched.get("tags", []), ensure_ascii=False),
                json.dumps({"resolution": parsed.get("resolution"), "video_codec": parsed.get("codec"), "audio_codec": parsed.get("audio"), "container": fpath.suffix[1:].upper()}, ensure_ascii=False),
                str(fpath), enriched.get("season", 0), enriched.get("episode", 0)
            ))
            imported_count += 1

    return {
        "success": True,
        "scanned_files": len(found_files),
        "imported_count": imported_count
    }
