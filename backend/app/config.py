import os
from pathlib import Path

# Base Paths
BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BACKEND_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "onyxvision.db"

# Frontend Web Build Path
FRONTEND_DIST_DIR = BACKEND_DIR.parent / "frontend" / "dist"

# Server Settings
HOST = os.getenv("ONYX_HOST", "0.0.0.0")
PORT = int(os.getenv("ONYX_PORT", "8000"))

# TMDB Scraper Settings
TMDB_API_KEY = os.getenv("ONYX_TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p"

# Streaming Buffer Settings
STREAM_CHUNK_SIZE = 2 * 1024 * 1024  # 2MB chunks for smooth seek
