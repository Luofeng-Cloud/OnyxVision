import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from app.database import get_db
from app.models import PlaybackProgressRequest, MarkPlayedRequest
from app.providers.emby import EmbyClient

logger = logging.getLogger("onyxvision.api.playback")
router = APIRouter(prefix="/api/playback", tags=["Playback & History"])

async def relay_progress_to_emby(
    source_row: Dict[str, Any],
    source_item_id: str,
    position_ticks: int,
    is_paused: bool,
    event: str
):
    """Background task to sync progress back to remote Emby / Jellyfin server."""
    try:
        client = EmbyClient(
            server_url=source_row["url"],
            api_key=source_row["api_key"],
            user_id=source_row["user_id"],
            username=source_row["username"],
            password=source_row["password"]
        )
        if event == "Stopped":
            await client.report_playback_stopped(source_item_id, position_ticks)
        elif event == "Start":
            await client.report_playback_start(source_item_id, position_ticks=position_ticks)
        else:
            await client.report_playback_progress(source_item_id, position_ticks, is_paused=is_paused, event=event)
    except Exception as e:
        logger.warning(f"Failed to relay progress to Emby: {e}")


@router.post("/progress")
async def update_playback_progress(req: PlaybackProgressRequest, background_tasks: BackgroundTasks):
    """
    Bidirectional playback progress synchronization.
    1. Updates local SQLite playback_history.
    2. Relays 10s heartbeat or stop event to Emby/Jellyfin server if item originated from Emby.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Check media item source and duration
        cursor.execute("SELECT source_id, source_item_id, duration FROM media_items WHERE id = ?", (req.item_id,))
        m_row = cursor.fetchone()
        if not m_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")

        source_id = m_row["source_id"]
        source_item_id = m_row["source_item_id"]
        db_duration = float(m_row["duration"] or 0)

        # Fall back to DB duration if client omitted duration_seconds
        duration = req.duration_seconds if (req.duration_seconds and req.duration_seconds > 0) else (db_duration if db_duration > 0 else 0)
        if duration > 0:
            percentage = min(100.0, max(0.0, (req.position_seconds / duration) * 100.0))
        else:
            percentage = 0.0

        # Consider watched if >= 92%
        is_played = 1 if percentage >= 92.0 else 0
        position_ticks = int(req.position_seconds * 10_000_000)

        hist_id = f"hist_{req.item_id}"
        cursor.execute("""
        INSERT INTO playback_history (
            id, item_id, source_id, source_item_id, position_ticks,
            position_seconds, duration_seconds, playback_percentage,
            is_played, play_count, last_played_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, CURRENT_TIMESTAMP
        )
        ON CONFLICT(item_id) DO UPDATE SET
            position_ticks = excluded.position_ticks,
            position_seconds = excluded.position_seconds,
            duration_seconds = excluded.duration_seconds,
            playback_percentage = excluded.playback_percentage,
            is_played = CASE WHEN excluded.is_played = 1 THEN 1 ELSE playback_history.is_played END,
            last_played_at = CURRENT_TIMESTAMP;
        """, (
            hist_id, req.item_id, source_id, source_item_id, position_ticks,
            req.position_seconds, duration, percentage, is_played
        ))

        # Check if source is Emby to relay
        if source_id and source_item_id:
            cursor.execute("SELECT * FROM sources WHERE id = ?", (source_id,))
            s_row = cursor.fetchone()
            if s_row and s_row["type"] in ("emby", "jellyfin"):
                background_tasks.add_task(
                    relay_progress_to_emby,
                    dict(s_row),
                    source_item_id,
                    position_ticks,
                    req.is_paused,
                    req.event or "TimeUpdate"
                )

    return {
        "success": True,
        "item_id": req.item_id,
        "position_seconds": req.position_seconds,
        "duration_seconds": req.duration_seconds,
        "playback_percentage": round(percentage, 1),
        "is_played": bool(is_played)
    }


@router.post("/mark-played")
async def mark_item_played(req: MarkPlayedRequest, background_tasks: BackgroundTasks):
    """Marks an item as played or unplayed locally and on upstream Emby."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT source_id, source_item_id, duration FROM media_items WHERE id = ?", (req.item_id,))
        m_row = cursor.fetchone()
        if not m_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")

        source_id = m_row["source_id"]
        source_item_id = m_row["source_item_id"]
        dur = float(m_row["duration"] or 100)

        pos_sec = dur if req.is_played else 0.0
        pct = 100.0 if req.is_played else 0.0
        ticks = int(pos_sec * 10_000_000)

        hist_id = f"hist_{req.item_id}"
        cursor.execute("""
        INSERT INTO playback_history (
            id, item_id, source_id, source_item_id, position_ticks,
            position_seconds, duration_seconds, playback_percentage,
            is_played, play_count, last_played_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, CURRENT_TIMESTAMP
        )
        ON CONFLICT(item_id) DO UPDATE SET
            position_ticks = excluded.position_ticks,
            position_seconds = excluded.position_seconds,
            playback_percentage = excluded.playback_percentage,
            is_played = ?,
            last_played_at = CURRENT_TIMESTAMP;
        """, (
            hist_id, req.item_id, source_id, source_item_id, ticks,
            pos_sec, dur, pct, 1 if req.is_played else 0, 1 if req.is_played else 0
        ))

        # Relay to Emby
        if source_id and source_item_id:
            cursor.execute("SELECT * FROM sources WHERE id = ?", (source_id,))
            s_row = cursor.fetchone()
            if s_row and s_row["type"] in ("emby", "jellyfin"):
                async def relay_mark(s_dict, s_item_id, played):
                    c = EmbyClient(server_url=s_dict["url"], api_key=s_dict["api_key"], user_id=s_dict["user_id"])
                    if played:
                        await c.mark_played(s_item_id)
                    else:
                        await c.mark_unplayed(s_item_id)
                background_tasks.add_task(relay_mark, dict(s_row), source_item_id, req.is_played)

    return {"success": True, "item_id": req.item_id, "is_played": req.is_played}


@router.get("/history")
def get_playback_history(limit: int = 50):
    """Returns playback history records with associated media metadata."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT p.*, m.title, m.poster, m.backdrop, m.type as media_type, m.tags
        FROM playback_history p
        JOIN media_items m ON p.item_id = m.id
        ORDER BY p.last_played_at DESC
        LIMIT ?
        """, (limit,))
        
        rows = []
        for r in cursor.fetchall():
            d = dict(r)
            d["is_played"] = bool(d["is_played"])
            rows.append(d)

        return {"history": rows}
