from pathlib import Path
from fastapi import APIRouter, Request, HTTPException, status

from app.database import get_db
from app.streaming.streamer import create_local_file_stream_response, create_remote_proxy_stream_response

router = APIRouter(prefix="/api/stream", tags=["Streaming"])

@router.get("/{item_id}")
async def stream_media(item_id: str, request: Request):
    """
    High-performance media streaming gateway with HTTP 206 Range support.
    Supports both local files and remote streams (Emby / Jellyfin / CDN) with instant seek.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, local_path, stream_url FROM media_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")

        local_path = row["local_path"]
        stream_url = row["stream_url"]

    # 1. Check local file on server
    if local_path and Path(local_path).exists() and Path(local_path).is_file():
        return create_local_file_stream_response(local_path, request)

    # 2. Check remote stream URL (Emby direct play or CDN)
    if stream_url and (stream_url.startswith("http://") or stream_url.startswith("https://")):
        return await create_remote_proxy_stream_response(stream_url, request)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No playable stream or file available for this media item."
    )
