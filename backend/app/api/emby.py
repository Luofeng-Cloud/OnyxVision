import json
import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from app.database import get_db
from app.models import EmbyConnectRequest, EmbySyncRequest
from app.providers.emby import EmbyClient

logger = logging.getLogger("onyxvision.api.emby")
router = APIRouter(prefix="/api/emby", tags=["Emby & Jellyfin"])

@router.post("/test")
async def test_emby_connection(req: EmbyConnectRequest):
    """
    Tests connectivity to an Emby or Jellyfin server.
    Verifies server reachability and credentials if provided.
    Probes movie and series totals, providing robust defaults/estimates on failure or disconnection.
    """
    client = EmbyClient(
        server_url=req.server_url,
        api_key=req.api_key,
        username=req.username,
        password=req.password
    )

    # 1. Test basic reachability
    test_res = await client.test_connection()
    if not test_res.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无法连接到 Emby 服务器: {test_res.get('error', '连接超时或服务器地址无效')}"
        )

    auth_data = None
    # If username or password provided, verify authentication
    if req.username or req.api_key:
        auth_res = await client.authenticate()
        if not auth_res.get("success"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Emby 身份鉴权失败: {auth_res.get('error', '用户名或密码错误')}"
            )
        auth_data = auth_res

    # 2. Probe movie and series counts
    movie_count = 0
    series_count = 0
    try:
        counts = await client.get_item_counts()
        movie_count = counts.get("movie_count", 0)
        series_count = counts.get("series_count", 0)
    except Exception as e:
        logger.warning(f"Could not probe Emby counts: {e}")

    server_name = test_res.get("server_name") or req.name or "Emby Server"
    version = test_res.get("version", "Unknown")
    operating_system = test_res.get("operating_system", "Linux")

    return {
        "success": True,
        "server_name": server_name,
        "version": version,
        "operating_system": operating_system,
        "authenticated": auth_data is not None,
        "user_id": auth_data.get("user_id") if auth_data else None,
        "access_token": auth_data.get("access_token") if auth_data else None,
        "movie_count": movie_count,
        "series_count": series_count,
        "is_offline": False
    }


@router.post("/connect")
async def connect_and_mount_emby(req: EmbyConnectRequest):
    """
    Authenticates, mounts, and saves an Emby/Jellyfin server as a media source.
    Returns list of available library views (e.g. Movies, TV Shows).
    Probes movie and series counts and saves them into extra metadata.
    """
    client = EmbyClient(
        server_url=req.server_url,
        api_key=req.api_key,
        username=req.username,
        password=req.password
    )

    auth_res = await client.authenticate()
    if not auth_res.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED if "401" in str(auth_res.get("error", "")) else status.HTTP_400_BAD_REQUEST,
            detail=f"Emby 服务器连接或鉴权失败: {auth_res.get('error', '请检查服务器地址、端口及账号密码')}"
        )

    # Fetch views / libraries
    views = []
    try:
        views = await client.get_views()
    except Exception as e:
        logger.warning(f"Failed to fetch views: {e}")

    # Probe movie and series counts
    movie_count = 0
    series_count = 0
    try:
        counts = await client.get_item_counts()
        movie_count = counts.get("movie_count", 0)
        series_count = counts.get("series_count", 0)
    except Exception as e:
        logger.warning(f"Failed to probe Emby counts: {e}")

    source_name = req.name or auth_res.get("server_name") or "Emby Server"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    extra_payload = {
        "views": views,
        "movie_count": movie_count,
        "series_count": series_count,
        "last_sync_time": now_str
    }

    clean_url = req.server_url.rstrip("/")
    clean_username = req.username or ""

    # Save to sources database (Check if same URL & username exists to prevent duplicates)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM sources WHERE url = ? AND username = ?", (clean_url, clean_username))
        existing_src = cursor.fetchone()
        if existing_src:
            source_id = existing_src["id"]
            cursor.execute("""
            UPDATE sources SET
                name = ?, api_key = ?, user_id = ?, password = ?, extra = ?, status = 'active', item_count = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (
                source_name,
                auth_res.get("access_token", ""),
                auth_res.get("user_id", ""),
                req.password or "",
                json.dumps(extra_payload, ensure_ascii=False),
                movie_count + series_count,
                source_id
            ))
        else:
            source_id = f"source_emby_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
            INSERT INTO sources (
                id, name, type, url, username, password, api_key, user_id, extra, status, item_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                source_id,
                source_name,
                "emby",
                clean_url,
                clean_username,
                req.password or "",
                auth_res.get("access_token", ""),
                auth_res.get("user_id", ""),
                json.dumps(extra_payload, ensure_ascii=False),
                "active",
                movie_count + series_count
            ))

    return {
        "success": True,
        "source_id": source_id,
        "name": source_name,
        "server_name": auth_res.get("server_name"),
        "user_id": auth_res.get("user_id"),
        "views": views,
        "movie_count": movie_count,
        "series_count": series_count,
        "last_sync_time": now_str
    }


@router.post("/sync")
async def sync_emby_media(req: EmbySyncRequest):
    """
    Synchronizes media items from an Emby media source into OnyxVision's local database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sources WHERE id = ?", (req.source_id,))
        src_row = cursor.fetchone()
        if not src_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")

    client = EmbyClient(
        server_url=src_row["url"],
        api_key=src_row["api_key"],
        user_id=src_row["user_id"],
        username=src_row["username"],
        password=src_row["password"]
    )

    try:
        views = await client.get_views()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch views: {e}")

    # Determine which view IDs to sync
    target_view_ids = req.view_ids or [v.get("Id") for v in views if v.get("Id")]
    synced_count = 0

    with get_db() as conn:
        cursor = conn.cursor()
        for v_id in target_view_ids:
            try:
                items = await client.get_items(parent_id=v_id, item_types="Movie,Series", limit=200)
                for it in items:
                    v_item = client.to_onyx_item(it, req.source_id)
                    cursor.execute("""
                    INSERT OR REPLACE INTO media_items (
                        id, source_id, source_item_id, type, title, original_title, year,
                        overview, tagline, poster, backdrop, banner, logo, rating,
                        community_rating, genres, actors, directors, duration, release_date,
                        ambient_color, tags, technical_info, stream_url, parent_id,
                        series_id, season_number, episode_number, is_favorite
                    ) VALUES (
                        :id, :source_id, :source_item_id, :type, :title, :original_title, :year,
                        :overview, :tagline, :poster, :backdrop, :banner, :logo, :rating,
                        :community_rating, :genres, :actors, :directors, :duration, :release_date,
                        :ambient_color, :tags, :technical_info, :stream_url, :parent_id,
                        :series_id, :season_number, :episode_number, :is_favorite
                    )
                    """, v_item)
                    synced_count += 1
            except Exception as e:
                logger.error(f"Error syncing view {v_id}: {e}")

        # Update source item count and last_sync_time in extra
        cursor.execute("SELECT extra FROM sources WHERE id = ?", (req.source_id,))
        s_row = cursor.fetchone()
        extra_data = {}
        if s_row and s_row["extra"]:
            try:
                extra_data = json.loads(s_row["extra"])
            except Exception:
                pass
        extra_data["last_sync_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("UPDATE sources SET item_count = ?, extra = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (synced_count, json.dumps(extra_data, ensure_ascii=False), req.source_id))

    return {
        "success": True,
        "source_id": req.source_id,
        "synced_items_count": synced_count
    }
