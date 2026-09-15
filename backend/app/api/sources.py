import json
import uuid
from typing import Dict, Any
from pathlib import Path
from fastapi import APIRouter, HTTPException, status

from app.database import get_db
from app.models import SourceCreateRequest

router = APIRouter(prefix="/api/sources", tags=["Media Sources"])

def mask_source_credentials(row: Dict[str, Any]) -> Dict[str, Any]:
    """Hides sensitive passwords and tokens from API output."""
    data = dict(row)
    if data.get("password"):
        data["password"] = "******"
    if data.get("api_key"):
        data["api_key"] = f"{data['api_key'][:4]}...{data['api_key'][-4:]}" if len(data["api_key"]) > 8 else "******"
    if data.get("extra"):
        try:
            extra_dict = json.loads(data["extra"]) if isinstance(data["extra"], str) else data["extra"]
            data["extra"] = extra_dict
            if isinstance(extra_dict, dict):
                data["movie_count"] = extra_dict.get("movie_count", 0)
                data["series_count"] = extra_dict.get("series_count", 0)
                data["last_sync_time"] = extra_dict.get("last_sync_time")
        except Exception:
            data["extra"] = {}
    return data

@router.get("")
def list_sources():
    """Returns all mounted media sources (Emby, WebDAV, Local, etc.)."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sources ORDER BY created_at ASC")
        rows = [mask_source_credentials(r) for r in cursor.fetchall()]
        return {"sources": rows}


@router.post("")
def create_source(req: SourceCreateRequest):
    """
    Mounts a new media source.
    Supports local folders, WebDAV shares, and Emby/Jellyfin servers.
    """
    source_type = req.type.lower()
    if source_type not in ("emby", "jellyfin", "webdav", "local"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported source type: {req.type}. Supported types: emby, jellyfin, webdav, local"
        )

    # Validate local directory path
    if source_type == "local" and req.url:
        p = Path(req.url)
        if not p.exists() or not p.is_dir():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Local path does not exist or is not a directory: {req.url}"
            )

    source_id = f"source_{source_type}_{uuid.uuid4().hex[:8]}"

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO sources (
            id, name, type, url, username, password, api_key, extra, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            source_id,
            req.name,
            source_type,
            req.url or "",
            req.username or "",
            req.password or "",
            req.api_key or "",
            json.dumps(req.extra or {}, ensure_ascii=False),
            "active"
        ))

    return {
        "success": True,
        "source_id": source_id,
        "name": req.name,
        "type": source_type,
        "status": "active"
    }


@router.get("/{source_id}")
def get_source_detail(source_id: str):
    """Retrieves specific media source configuration and statistics."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sources WHERE id = ?", (source_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
        
        # Count items
        cursor.execute("SELECT COUNT(*) FROM media_items WHERE source_id = ?", (source_id,))
        cached_count = cursor.fetchone()[0]

        data = mask_source_credentials(row)
        data["cached_item_count"] = cached_count
        if not data.get("item_count"):
            data["item_count"] = cached_count
        return data


@router.delete("/{source_id}")
def delete_source(source_id: str):
    """
    Unmounts and removes a media source.
    Automatically cascades deletion to all cached media items and history.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM sources WHERE id = ?", (source_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")

        # Delete associated media items, playback history, and source
        cursor.execute("DELETE FROM playback_history WHERE source_id = ?", (source_id,))
        cursor.execute("DELETE FROM media_items WHERE source_id = ?", (source_id,))
        cursor.execute("DELETE FROM sources WHERE id = ?", (source_id,))

        return {"success": True, "message": f"Source {source_id} deleted successfully."}
