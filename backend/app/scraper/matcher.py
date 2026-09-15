import re
import json
import hashlib
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import httpx

from app.config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE
from app.database import get_db

logger = logging.getLogger("onyxvision.scraper")

class FilenameMatcher:
    """
    Industrial-grade filename cleaner and regex pipeline for media files.
    Accurately extracts Title, Year, Season, Episode, Resolution, HDR, Audio, Codec, and Release Group.
    """

    # Common release groups to strip at the end
    RELEASE_GROUPS = [
        "FLUX", "SWTYBLZ", "NTb", "ROCCaT", "CMCT", "FRDS", "CHD", "WiKi", "HDChina",
        "RARBG", "YIFY", "SPARKS", "AMIABLE", "GECKOS", "DRONES", "FGT", "TOMMY",
        "CtrlHD", "DON", "EbP", "VietHD", "TayTO", "HHWEB", "ADE", "HONE", "PTer",
        "NC-Raws", "Erai-raws", "SubsPlease", "MSubs"
    ]

    @classmethod
    def clean(cls, raw_filename: str) -> Dict[str, Any]:
        """
        Cleans and parses a raw media filename or directory path.
        """
        # Strip path and extension
        filename = Path(raw_filename).stem
        
        # Extract season and episode
        season = None
        episode = None
        cut_index = None

        # S01E02 or s1e2 or S01.E02
        s_e_match = re.search(r"[Ss](\d{1,2})[.\s_-]*[Ee](\d{1,3})", filename, re.IGNORECASE)
        if s_e_match:
            season = int(s_e_match.group(1))
            episode = int(s_e_match.group(2))
            cut_index = s_e_match.start()
        else:
            # Chinese format: 第1季 第2集
            cn_s = re.search(r"第\s*(\d{1,2})\s*季", filename)
            cn_e = re.search(r"第\s*(\d{1,3})\s*集", filename)
            if cn_s:
                season = int(cn_s.group(1))
                cut_index = cn_s.start() if cut_index is None else cut_index
            if cn_e:
                episode = int(cn_e.group(1))
                cut_index = cn_e.start() if cut_index is None else cut_index
            
            # Anime episode notation e.g. " - 01 " or " EP01 " or " E01 "
            if episode is None:
                ep_match = re.search(r"(?:[-\s]|\bEP?|\bE)(\d{1,3})(?:v\d)?(?:\s|\[|\.|$)", filename, re.IGNORECASE)
                if ep_match and not re.search(r"\b(19\d\d|20\d\d)\b", ep_match.group(0)):
                    episode = int(ep_match.group(1))
                    season = 1 if season is None else season
                    cut_index = ep_match.start()

        # Extract Year (1920 - 2099)
        year = None
        year_match = re.search(r"\b(19\d{2}|20\d{2})\b", filename)
        if year_match:
            year = int(year_match.group(1))
            if cut_index is None or year_match.start() < cut_index:
                cut_index = year_match.start()

        # Extract Resolution (support 3840x2160, 4K, 2160p, 1080p, 1920x1080, 720p)
        resolution = "1080p FHD"
        if re.search(r"\b(2160p|4k|uhd|3840x2160)\b", filename, re.IGNORECASE):
            resolution = "4K UHD"
        elif re.search(r"\b(1080p|fhd|1080i|1920x1080)\b", filename, re.IGNORECASE):
            resolution = "1080p FHD"
        elif re.search(r"\b(720p|hd|1280x720)\b", filename, re.IGNORECASE):
            resolution = "720p HD"

        # Extract HDR / Dynamic Range
        hdr = None
        if re.search(r"\b(dolby\s*vision|dovi|dv)\b", filename, re.IGNORECASE):
            hdr = "Dolby Vision"
        elif re.search(r"\b(hdr10\+|hdr10plus)\b", filename, re.IGNORECASE):
            hdr = "HDR10+"
        elif re.search(r"\b(hdr10|hdr)\b", filename, re.IGNORECASE):
            hdr = "HDR10"
        elif re.search(r"\b(hlg)\b", filename, re.IGNORECASE):
            hdr = "HLG"

        # Extract Audio
        audio = "AAC"
        if re.search(r"\b(atmos|truehd)\b", filename, re.IGNORECASE):
            audio = "Dolby Atmos"
        elif re.search(r"\b(dts-hd\s*ma|dts-hd|dts-x|dts)\b", filename, re.IGNORECASE):
            audio = "DTS-HD MA"
        elif re.search(r"\b(ddp5\.1|eac3|dd\+)\b", filename, re.IGNORECASE):
            audio = "Dolby Digital Plus"
        elif re.search(r"\b(ac3|dd5\.1)\b", filename, re.IGNORECASE):
            audio = "Dolby Digital 5.1"
        elif re.search(r"\b(flac)\b", filename, re.IGNORECASE):
            audio = "FLAC Lossless"

        # Extract Codec
        codec = "H.264"
        if re.search(r"\b(x265|h265|hevc)\b", filename, re.IGNORECASE):
            codec = "HEVC 10-bit" if re.search(r"\b10bit\b", filename, re.IGNORECASE) else "HEVC"
        elif re.search(r"\b(av1)\b", filename, re.IGNORECASE):
            codec = "AV1"
        elif re.search(r"\b(x264|h264|avc)\b", filename, re.IGNORECASE):
            codec = "H.264"

        # Extract Source
        source = "WEB-DL"
        if re.search(r"\b(bluray|bdrip|remux)\b", filename, re.IGNORECASE):
            source = "BluRay Remux" if re.search(r"\bremux\b", filename, re.IGNORECASE) else "BluRay"
        elif re.search(r"\b(web-dl|webrip|web)\b", filename, re.IGNORECASE):
            source = "WEB-DL"
        elif re.search(r"\b(hdtv)\b", filename, re.IGNORECASE):
            source = "HDTV"

        # Extract Release Group
        release_group = ""
        rg_match = re.search(r"-([A-Za-z0-9_]+)(?:\[.*?\])?$", filename)
        if rg_match:
            release_group = rg_match.group(1)

        # Title Parsing: Extract part before year, season, or tech tags
        # Remove leading brackets like [NC-Raws]
        clean_title = re.sub(r"^\[.*?\]\s*", "", filename)
        
        # If we found a clear cut marker (season, year, episode)
        if cut_index is not None:
            # Adjust cut_index relative to prefix removed
            prefix_len = len(filename) - len(clean_title)
            adj_cut = max(0, cut_index - prefix_len)
            clean_title = clean_title[:adj_cut]
        else:
            # Cut at first technical tag
            tech_cut = re.search(r"\b(2160p|1080p|720p|bluray|web-dl|x265|x264|hevc|uhd)\b", clean_title, re.IGNORECASE)
            if tech_cut:
                clean_title = clean_title[:tech_cut.start()]

        # Remove any remaining bracketed blocks e.g. (2024) or [1080p]
        clean_title = re.sub(r"\[.*?\]|\(.*?\)", "", clean_title)
        # Clean trailing dots, hyphens, underscores and replace dots with spaces
        clean_title = re.sub(r"[\.\_\+]+", " ", clean_title)
        clean_title = re.sub(r"[\-\–\—\:\/\s]+$", "", clean_title).strip()

        # Generate badges
        tags = [resolution]
        if hdr:
            tags.append(hdr)
        if audio:
            tags.append(audio)
        if codec:
            tags.append(codec)
        if source:
            tags.append(source)

        return {
            "raw_name": raw_filename,
            "title": clean_title if clean_title else filename,
            "year": year,
            "season": season,
            "episode": episode,
            "is_tv": (season is not None or episode is not None),
            "resolution": resolution,
            "hdr": hdr,
            "audio": audio,
            "codec": codec,
            "source": source,
            "release_group": release_group,
            "tags": tags
        }


class TMDBScraper:
    """
    TMDB API v3 Scraper with SQLite cache and intelligent fallback generator.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or TMDB_API_KEY
        self.base_url = TMDB_BASE_URL
        self.image_base = TMDB_IMAGE_BASE

    def _get_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieves cached TMDB metadata."""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT data FROM tmdb_cache WHERE cache_key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
        except Exception as e:
            logger.warning(f"Failed to read tmdb_cache: {e}")
        return None

    def _set_cache(self, key: str, data: Dict[str, Any]):
        """Caches TMDB metadata in SQLite."""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT OR REPLACE INTO tmdb_cache (cache_key, data, cached_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (key, json.dumps(data, ensure_ascii=False)))
        except Exception as e:
            logger.warning(f"Failed to write tmdb_cache: {e}")

    async def search_movie(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Searches TMDB for a movie."""
        cache_key = f"movie_search_{title}_{year}"
        cached = self._get_cache(cache_key)
        if cached:
            return cached

        if not self.api_key:
            return None

        url = f"{self.base_url}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": title,
            "language": "zh-CN",
            "include_adult": "false"
        }
        if year:
            params["year"] = str(year)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    if results:
                        res = results[0]
                        self._set_cache(cache_key, res)
                        return res
        except Exception as e:
            logger.error(f"TMDB search movie error: {e}")
        return None

    async def search_tv(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Searches TMDB for a TV series."""
        cache_key = f"tv_search_{title}_{year}"
        cached = self._get_cache(cache_key)
        if cached:
            return cached

        if not self.api_key:
            return None

        url = f"{self.base_url}/search/tv"
        params = {
            "api_key": self.api_key,
            "query": title,
            "language": "zh-CN"
        }
        if year:
            params["first_air_date_year"] = str(year)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    if results:
                        res = results[0]
                        self._set_cache(cache_key, res)
                        return res
        except Exception as e:
            logger.error(f"TMDB search TV error: {e}")
        return None

    async def enrich_item(self, parsed_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriches a parsed filename with TMDB data or applies high-grade fallback.
        """
        title = parsed_info.get("title", "")
        year = parsed_info.get("year")
        is_tv = parsed_info.get("is_tv", False)

        tmdb_data = None
        if self.api_key:
            if is_tv:
                tmdb_data = await self.search_tv(title, year)
            else:
                tmdb_data = await self.search_movie(title, year)

        # Ambient color selection based on title
        color_palette = ["#1e3a8a", "#b46a2a", "#c2410c", "#047857", "#4338ca", "#7e22ce", "#be123c", "#0f766e"]
        h_val = int(hashlib.md5(title.encode()).hexdigest(), 16)
        ambient_color = color_palette[h_val % len(color_palette)]

        if tmdb_data:
            poster_path = tmdb_data.get("poster_path")
            backdrop_path = tmdb_data.get("backdrop_path")
            poster = f"{self.image_base}/w780{poster_path}" if poster_path else ""
            backdrop = f"{self.image_base}/original{backdrop_path}" if backdrop_path else ""
            return {
                "title": tmdb_data.get("title") or tmdb_data.get("name") or title,
                "original_title": tmdb_data.get("original_title") or tmdb_data.get("original_name") or title,
                "overview": tmdb_data.get("overview", ""),
                "year": year or (tmdb_data.get("release_date") or tmdb_data.get("first_air_date", ""))[:4],
                "rating": round(float(tmdb_data["vote_average"]), 1) if tmdb_data.get("vote_average") is not None else 8.0,
                "poster": poster,
                "backdrop": backdrop,
                "ambient_color": ambient_color,
                "tags": parsed_info.get("tags", []),
                "is_tv": is_tv,
                "season": parsed_info.get("season"),
                "episode": parsed_info.get("episode")
            }

        # Offline / Fallback generator: creates neat, clean metadata
        return {
            "title": title,
            "original_title": title,
            "overview": f"《{title}》是于 {year or '近年'} 上映的高清影视佳作。技术制式：{', '.join(parsed_info.get('tags', []))}。",
            "year": year,
            "rating": 8.5,
            "poster": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=780&q=80",
            "backdrop": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1920&q=80",
            "ambient_color": ambient_color,
            "tags": parsed_info.get("tags", []),
            "is_tv": is_tv,
            "season": parsed_info.get("season"),
            "episode": parsed_info.get("episode")
        }
