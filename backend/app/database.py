import sqlite3
from contextlib import contextmanager

from app.config import DB_PATH

def get_connection() -> sqlite3.Connection:
    """Creates a database connection with WAL mode and row factory enabled."""
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

@contextmanager
def get_db():
    """Context manager for SQLite database operations with auto-commit."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initializes the database schema and seeds demo media if empty."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Sources table (Emby, Jellyfin, WebDAV, Local)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL, -- emby, jellyfin, webdav, local
            url TEXT,
            username TEXT,
            password TEXT,
            api_key TEXT,
            user_id TEXT,
            extra TEXT, -- JSON string for headers, mount points, etc.
            status TEXT DEFAULT 'active',
            item_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. Media items table (Movies, TV Series, Seasons, Episodes)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS media_items (
            id TEXT PRIMARY KEY,
            source_id TEXT,
            source_item_id TEXT,
            type TEXT NOT NULL, -- movie, series, season, episode
            title TEXT NOT NULL,
            original_title TEXT,
            year INTEGER,
            overview TEXT,
            tagline TEXT,
            poster TEXT,
            backdrop TEXT,
            banner TEXT,
            logo TEXT,
            rating REAL DEFAULT 0.0,
            community_rating REAL DEFAULT 0.0,
            genres TEXT, -- JSON array: ["科幻", "动作"]
            actors TEXT, -- JSON array of objects: [{"name": "...", "role": "...", "thumb": "..."}]
            directors TEXT, -- JSON array: ["丹尼斯·维伦纽瓦"]
            duration INTEGER DEFAULT 0, -- in seconds
            release_date TEXT,
            ambient_color TEXT DEFAULT '#1e293b', -- Hex color for UI ambient glow
            tags TEXT, -- JSON array: ["4K UHD", "Dolby Vision", "Dolby Atmos"]
            technical_info TEXT, -- JSON object: {resolution, codec, audio_codec, bitrate, container, aspect_ratio, fps}
            stream_url TEXT, -- Direct play URL or proxy URL
            local_path TEXT,
            parent_id TEXT, -- Series ID for seasons/episodes
            series_id TEXT, -- Series ID for episodes
            season_number INTEGER DEFAULT 0,
            episode_number INTEGER DEFAULT 0,
            is_favorite BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE
        );
        """)

        # 3. Playback history table (tracks positions, durations, played status)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS playback_history (
            id TEXT PRIMARY KEY,
            item_id TEXT NOT NULL UNIQUE,
            source_id TEXT,
            source_item_id TEXT,
            position_ticks INTEGER DEFAULT 0, -- Emby ticks: 10,000,000 per second
            position_seconds REAL DEFAULT 0.0,
            duration_seconds REAL DEFAULT 0.0,
            playback_percentage REAL DEFAULT 0.0,
            is_played BOOLEAN DEFAULT 0,
            play_count INTEGER DEFAULT 0,
            last_played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES media_items(id) ON DELETE CASCADE
        );
        """)

        # 4. TMDB scraper cache table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tmdb_cache (
            cache_key TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Database initialized with clean tables. Sources and media items will be added dynamically by the user.
        conn.commit()
