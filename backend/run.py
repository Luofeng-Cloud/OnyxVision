import sys
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print(f"[OnyxVision Launcher] Starting OnyxVision Core Backend on {HOST}:{PORT}...")
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info"
    )
