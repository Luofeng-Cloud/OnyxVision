import mimetypes
import logging
from pathlib import Path
from typing import Generator, Tuple
from fastapi import Request, HTTPException, status
from fastapi.responses import StreamingResponse, Response
import httpx

from app.config import STREAM_CHUNK_SIZE

logger = logging.getLogger("onyxvision.streamer")

def parse_byte_range(range_header: str, file_size: int) -> Tuple[int, int]:
    """
    Parses a Range header (e.g. 'bytes=100-200' or 'bytes=100-') into (start, end).
    """
    if not range_header.startswith("bytes="):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Range header format."
        )

    range_val = range_header.replace("bytes=", "").strip()
    parts = range_val.split("-")
    
    if len(parts) != 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid byte range.")

    start_str, end_str = parts[0].strip(), parts[1].strip()

    if not start_str and not end_str:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid empty range.")

    try:
        if start_str and end_str:
            start = int(start_str)
            end = int(end_str)
        elif start_str:
            start = int(start_str)
            end = min(start + STREAM_CHUNK_SIZE - 1, file_size - 1)
        else:  # Suffix byte range: bytes=-500 (last 500 bytes)
            length = int(end_str)
            start = max(0, file_size - length)
            end = file_size - 1
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid numeric value in Range header.")

    if start >= file_size or start < 0 or end < start:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail="Requested range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"}
        )

    end = min(end, file_size - 1)
    return start, end


def stream_file_chunk(file_path: str, start: int, content_length: int, chunk_size: int = 128 * 1024) -> Generator[bytes, None, None]:
    """
    Reads a local file starting at 'start' for 'content_length' bytes in chunks.
    """
    bytes_remaining = content_length
    with open(file_path, "rb") as f:
        f.seek(start)
        while bytes_remaining > 0:
            bytes_to_read = min(bytes_remaining, chunk_size)
            chunk = f.read(bytes_to_read)
            if not chunk:
                break
            bytes_remaining -= len(chunk)
            yield chunk


def create_local_file_stream_response(file_path: str, request: Request) -> Response:
    """
    Creates an HTTP 206 Partial Content or 200 StreamingResponse for local video files.
    Enables millisecond-accurate seek, scrub, and instant resume.
    """
    path_obj = Path(file_path)
    if not path_obj.exists() or not path_obj.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media file not found on server.")

    file_size = path_obj.stat().st_size
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        ext = path_obj.suffix.lower()
        if ext in (".mkv", ".webm"):
            mime_type = "video/webm"
        elif ext == ".mp4":
            mime_type = "video/mp4"
        elif ext in (".ts", ".m2ts"):
            mime_type = "video/mp2t"
        else:
            mime_type = "video/mp4"

    range_header = request.headers.get("range")

    if range_header:
        start, end = parse_byte_range(range_header, file_size)
        content_length = (end - start) + 1
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Content-Type": mime_type,
            "Cache-Control": "no-cache"
        }
        return StreamingResponse(
            stream_file_chunk(file_path, start, content_length),
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            headers=headers
        )
    else:
        # Initial request without range: send first chunk or full stream with Accept-Ranges
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
            "Content-Type": mime_type,
            "Cache-Control": "no-cache"
        }
        return StreamingResponse(
            stream_file_chunk(file_path, 0, file_size),
            status_code=status.HTTP_200_OK,
            headers=headers
        )


async def create_remote_proxy_stream_response(remote_url: str, request: Request) -> Response:
    """
    Transparently proxies HTTP 206 Range requests to remote video streams (e.g. Emby/Jellyfin/CDN).
    """
    range_header = request.headers.get("range", "bytes=0-")
    proxy_headers = {
        "Range": range_header,
        "User-Agent": request.headers.get("user-agent", "OnyxVision-Streamer/1.0")
    }

    client = httpx.AsyncClient(timeout=30.0, verify=False, follow_redirects=True)
    try:
        remote_req = client.build_request("GET", remote_url, headers=proxy_headers)
        remote_resp = await client.send(remote_req, stream=True)

        async def remote_stream_generator():
            try:
                async for chunk in remote_resp.aiter_bytes(chunk_size=128 * 1024):
                    yield chunk
            finally:
                await remote_resp.aclose()
                await client.aclose()

        response_headers = {
            "Accept-Ranges": remote_resp.headers.get("accept-ranges", "bytes"),
            "Content-Type": remote_resp.headers.get("content-type", "video/mp4"),
            "Cache-Control": "no-cache"
        }
        if "content-range" in remote_resp.headers:
            response_headers["Content-Range"] = remote_resp.headers["content-range"]
        if "content-length" in remote_resp.headers:
            response_headers["Content-Length"] = remote_resp.headers["content-length"]

        status_code = remote_resp.status_code if remote_resp.status_code in (200, 206) else 206
        return StreamingResponse(
            remote_stream_generator(),
            status_code=status_code,
            headers=response_headers
        )
    except Exception as e:
        await client.aclose()
        logger.error(f"Remote stream proxy error: {e}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Failed to proxy stream: {str(e)}")
