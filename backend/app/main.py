import socket
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.config import PORT, FRONTEND_DIST_DIR, DB_PATH
from app.database import init_db, get_db
from app.api import media, emby, sources, playback, stream

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("onyxvision.main")

def get_lan_ip() -> str:
    """Detects the primary LAN IP address for mobile and local network access."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.5)
            # Does not actually create connection, just routes socket to determine interface
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def print_startup_banner(lan_ip: str, port: int):
    """Prints a clean, stylish startup banner to console."""
    banner = f"""
======================================================================
  ██████╗ ███╗   ██╗██╗   ██╗██╗  ██╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
 ██╔═══██╗████╗  ██║╚██╗ ██╔╝╚██╗██╔╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
 ██║   ██║██╔██╗ ██║ ╚████╔╝  ╚███╔╝ ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
 ██║   ██║██║╚██╗██║  ╚██╔╝   ██╔██╗ ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
 ╚██████╔╝██║ ╚████║   ██║   ██╔╝ ██╗ ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
       ONYXVISION CORE ENGINE v1.0.0 · 曜石视界 私有流媒体中枢
----------------------------------------------------------------------
  * 本地 Web 播放 (Local):     http://127.0.0.1:{port}
  * 局域网 / 移动 (LAN):       http://{lan_ip}:{port}
  * API 交互文档 (Swagger):    http://127.0.0.1:{port}/docs
  * 规范架构文档 (ReDoc):      http://127.0.0.1:{port}/redoc
  * 曜石视界数据库:            {DB_PATH} (WAL 极速高并发)
======================================================================
"""
    print(banner)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown initialization."""
    # 1. Initialize SQLite schema & seed demo media
    init_db()

    # 2. Print network access banner
    lan_ip = get_lan_ip()
    print_startup_banner(lan_ip, PORT)

    yield

    logger.info("OnyxVision Core Engine shutting down gracefully.")


app = FastAPI(
    title="OnyxVision Core Engine API",
    description="Obsidian-Deep Private Streaming Hub · 曜石视界流媒体中枢",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend dev servers and mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Core API Routers
app.include_router(media.router)
app.include_router(emby.router)
app.include_router(sources.router)
app.include_router(playback.router)
app.include_router(stream.router)

# Check if frontend distribution build exists
if FRONTEND_DIST_DIR.exists() and (FRONTEND_DIST_DIR / "index.html").exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST_DIR), html=True), name="frontend")
else:
    @app.get("/", response_class=HTMLResponse)
    def welcome_page():
        """Modern OnyxVision-styled welcome dashboard when frontend dist is not mounted."""
        lan_ip = get_lan_ip()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM media_items WHERE type IN ('movie', 'series')")
            media_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM sources")
            source_count = cursor.fetchone()[0]

        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OnyxVision Core Engine · 曜石视界服务就绪</title>
    <style>
        :root {{
            --bg-primary: #07060b;
            --bg-card: rgba(18, 14, 28, 0.78);
            --border-card: rgba(168, 85, 247, 0.18);
            --accent: #a855f7;
            --accent-glow: rgba(168, 85, 247, 0.4);
            --accent-gradient: linear-gradient(135deg, #a855f7, #6366f1);
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", sans-serif; }}
        body {{
            background-color: var(--bg-primary);
            background-image: radial-gradient(circle at 50% 15%, rgba(168, 85, 247, 0.18), transparent 60%),
                              radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.12), transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }}
        .container {{
            max-width: 880px;
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            backdrop-filter: blur(24px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65), 0 0 40px rgba(168, 85, 247, 0.08);
        }}
        .header {{
            display: flex;
            align-items: center;
            gap: 18px;
            margin-bottom: 24px;
        }}
        .logo-badge {{
            width: 58px;
            height: 58px;
            background: linear-gradient(135deg, #9333ea, #4f46e5);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            font-weight: 900;
            box-shadow: 0 8px 24px var(--accent-glow);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        h1 {{ font-size: 26px; font-weight: 800; letter-spacing: -0.5px; }}
        .badge-online {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(34, 197, 94, 0.3);
            margin-top: 4px;
        }}
        .badge-online::before {{
            content: '';
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow: 0 0 10px #22c55e;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 28px 0;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(168, 85, 247, 0.12);
            padding: 20px;
            border-radius: 14px;
            transition: border-color 0.2s;
        }}
        .stat-card:hover {{
            border-color: rgba(168, 85, 247, 0.35);
        }}
        .stat-value {{ font-size: 26px; font-weight: 800; color: #c084fc; }}
        .stat-label {{ font-size: 13px; color: var(--text-sub); margin-top: 4px; }}
        .links-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 24px;
        }}
        .btn {{
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(30, 26, 46, 0.8);
            color: #fff;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .btn:hover {{
            background: #2e2648;
            border-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: 0 4px 16px var(--accent-glow);
        }}
        .btn-primary {{
            background: var(--accent-gradient);
            border: none;
        }}
        .btn-primary:hover {{
            background: linear-gradient(135deg, #b06ef8, #7275f3);
            box-shadow: 0 6px 22px var(--accent-glow);
        }}
        .network-info {{
            margin-top: 32px;
            padding: 18px;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 13px;
            color: #cbd5e1;
            line-height: 1.9;
        }}
        .network-info span {{ color: #c084fc; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo-badge">💎</div>
            <div>
                <h1>OnyxVision Core Engine · 曜石视界服务运行中</h1>
                <div class="badge-online">FastAPI 曜石极速微服务引擎已在线 (WAL 模式)</div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{media_count} 部</div>
                <div class="stat-label">曜石影视片库 (4K HDR 示范)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{source_count} 个</div>
                <div class="stat-label">媒体源接入中枢 (Emby/本地/WebDAV)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">WAL 极速引擎</div>
                <div class="stat-label">SQLite 高并发晶体持久层</div>
            </div>
        </div>

        <div class="links-group">
            <a href="/docs" class="btn btn-primary" target="_blank">📖 打开 Swagger API 文档</a>
            <a href="/redoc" class="btn" target="_blank">📄 打开 ReDoc 文档</a>
            <a href="/api/media/home" class="btn" target="_blank">🎬 首页聚合数据接口 (/api/media/home)</a>
            <a href="/api/sources" class="btn" target="_blank">🔌 挂载源管理接口 (/api/sources)</a>
        </div>

        <div class="network-info">
            <div>📡 本机访问: <span>http://127.0.0.1:{PORT}</span></div>
            <div>📱 局域网 / 移动端访问: <span>http://{lan_ip}:{PORT}</span></div>
            <div>💎 曜石视界数据库: <span>{DB_PATH}</span></div>
            <div>📦 前端静态托管目录: <span>{FRONTEND_DIST_DIR}</span> (前端构建就绪后将自动接管)</div>
        </div>
    </div>
</body>
</html>
        """
        return HTMLResponse(content=html_content, status_code=200)
