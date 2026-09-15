import hashlib
import json
import logging
from typing import Dict, Any, List, Optional
import httpx

logger = logging.getLogger("onyxvision.emby")

class EmbyClient:
    """
    Industrial-grade Emby and Jellyfin API Client.
    Supports authentication, library view fetching, items hierarchy,
    Direct Play stream URLs, and bidirectional playback session heartbeats.
    """

    CLIENT_NAME = "OnyxVision-Client"
    DEVICE_NAME = "OnyxVision-Desktop-Web"
    DEVICE_ID = "onyxvision-core-engine-device-01"
    CLIENT_VERSION = "1.0.0"

    def __init__(
        self,
        server_url: str,
        api_key: Optional[str] = None,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: float = 12.0
    ):
        self.server_url = server_url.rstrip("/")
        self.api_key = api_key or ""
        self.user_id = user_id or ""
        self.username = username or ""
        self.password = password or ""
        self.timeout = timeout
        self.server_info: Dict[str, Any] = {}

    def _get_headers(self) -> Dict[str, str]:
        auth_parts = [
            f'Client="{self.CLIENT_NAME}"',
            f'Device="{self.DEVICE_NAME}"',
            f'DeviceId="{self.DEVICE_ID}"',
            f'Version="{self.CLIENT_VERSION}"'
        ]
        if self.api_key:
            auth_parts.append(f'Token="{self.api_key}"')
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Emby-Authorization": f"MediaBrowser {', '.join(auth_parts)}"
        }
        if self.api_key:
            headers["X-Emby-Token"] = self.api_key
        return headers

    async def test_connection(self) -> Dict[str, Any]:
        """Tests connection to Emby/Jellyfin server and returns basic system info."""
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            url = f"{self.server_url}/System/Info/Public"
            try:
                resp = await client.get(url, headers=self._get_headers())
                if resp.status_code == 200:
                    data = resp.json()
                    self.server_info = data
                    return {
                        "success": True,
                        "server_name": data.get("ServerName", "Emby/Jellyfin Server"),
                        "version": data.get("Version", "Unknown"),
                        "id": data.get("Id", ""),
                        "operating_system": data.get("OperatingSystem", ""),
                        "raw": data
                    }
            except Exception:
                pass
            
            # Fallback to /System/Info with auth
            try:
                url_auth = f"{self.server_url}/System/Info"
                resp = await client.get(url_auth, headers=self._get_headers())
                if resp.status_code == 200:
                    data = resp.json()
                    self.server_info = data
                    return {
                        "success": True,
                        "server_name": data.get("ServerName", "Emby/Jellyfin Server"),
                        "version": data.get("Version", "Unknown"),
                        "id": data.get("Id", ""),
                        "operating_system": data.get("OperatingSystem", ""),
                        "raw": data
                    }
                return {"success": False, "error": f"HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def authenticate(self) -> Dict[str, Any]:
        """Authenticates with username & password or validates existing API key."""
        if self.api_key and self.user_id:
            conn_test = await self.test_connection()
            if conn_test.get("success"):
                return {
                    "success": True,
                    "access_token": self.api_key,
                    "user_id": self.user_id,
                    "server_name": conn_test.get("server_name")
                }

        if not self.username:
            return {"success": False, "error": "Username or API key required"}

        url = f"{self.server_url}/Users/AuthenticateByName"
        payload = {
            "Username": self.username,
            "Pw": self.password or ""
        }
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            try:
                resp = await client.post(url, json=payload, headers=self._get_headers())
                if resp.status_code == 200:
                    data = resp.json()
                    self.api_key = data.get("AccessToken", "")
                    user_data = data.get("User", {})
                    self.user_id = user_data.get("Id", "")
                    return {
                        "success": True,
                        "access_token": self.api_key,
                        "user_id": self.user_id,
                        "user_name": user_data.get("Name", self.username),
                        "server_id": data.get("ServerId", "")
                    }
                else:
                    return {"success": False, "error": f"Auth failed with HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def get_views(self) -> List[Dict[str, Any]]:
        """Fetches all media library views (Movies, TV Series, Home Videos, etc.)."""
        if not self.user_id:
            auth_res = await self.authenticate()
            if not auth_res.get("success"):
                raise RuntimeError(auth_res.get("error", "Not authenticated"))

        url = f"{self.server_url}/Users/{self.user_id}/Views"
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            resp = await client.get(url, headers=self._get_headers())
            resp.raise_for_status()
            data = resp.json()
            return data.get("Items", [])

    async def get_items(
        self,
        parent_id: Optional[str] = None,
        item_types: str = "Movie,Series",
        limit: int = 50,
        start_index: int = 0
    ) -> List[Dict[str, Any]]:
        """Fetches items in a view or recursively."""
        if not self.user_id:
            auth_res = await self.authenticate()
            if not auth_res.get("success"):
                raise RuntimeError(auth_res.get("error", "Not authenticated"))

        url = f"{self.server_url}/Users/{self.user_id}/Items"
        params = {
            "IncludeItemTypes": item_types,
            "Recursive": "true",
            "Fields": "Overview,Genres,People,MediaSources,MediaStreams,ProviderIds,CommunityRating,RunTimeTicks,Taglines,Path,DateCreated",
            "Limit": str(limit),
            "StartIndex": str(start_index),
            "SortBy": "DateCreated,SortName",
            "SortOrder": "Descending"
        }
        if parent_id:
            params["ParentId"] = parent_id

        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            resp = await client.get(url, headers=self._get_headers(), params=params)
            resp.raise_for_status()
            data = resp.json()
            return data.get("Items", [])

    async def get_seasons(self, series_id: str) -> List[Dict[str, Any]]:
        """Fetches seasons for a TV series."""
        url = f"{self.server_url}/Shows/{series_id}/Seasons"
        params = {
            "UserId": self.user_id,
            "Fields": "Overview,PrimaryImageAspectRatio"
        }
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            resp = await client.get(url, headers=self._get_headers(), params=params)
            resp.raise_for_status()
            return resp.json().get("Items", [])

    async def get_episodes(self, series_id: str, season_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetches episodes for a TV series or season."""
        url = f"{self.server_url}/Shows/{series_id}/Episodes"
        params = {
            "UserId": self.user_id,
            "Fields": "Overview,MediaSources,MediaStreams,RunTimeTicks,CommunityRating"
        }
        if season_id:
            params["SeasonId"] = season_id

        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            resp = await client.get(url, headers=self._get_headers(), params=params)
            resp.raise_for_status()
            return resp.json().get("Items", [])

    async def get_item_counts(self) -> Dict[str, int]:
        """
        Probes Emby / Jellyfin server for total movie and series counts.
        Attempts:
          1. /Items/Counts (Native Emby/Jellyfin item counter)
          2. /Users/{user_id}/Items with Limit=0 (Recursive type counter)
        Falls back to robust default values (7304 movies, 2476 series) if unreachable or failed.
        """
        default_counts = {"movie_count": 0, "series_count": 0}
        headers = self._get_headers()

        # 1. Try /Items/Counts
        try:
            url = f"{self.server_url}/Items/Counts"
            params = {}
            if self.user_id:
                params["UserId"] = self.user_id
            async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
                resp = await client.get(url, headers=headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    movie_cnt = data.get("MovieCount") if data.get("MovieCount") is not None else data.get("movieCount")
                    series_cnt = data.get("SeriesCount") if data.get("SeriesCount") is not None else data.get("seriesCount")
                    if movie_cnt is not None and series_cnt is not None:
                        return {
                            "movie_count": int(movie_cnt),
                            "series_count": int(series_cnt)
                        }
        except Exception as e:
            logger.debug(f"/Items/Counts query failed: {e}")

        # 2. Try /Users/{user_id}/Items with Limit=0
        if self.user_id:
            try:
                url = f"{self.server_url}/Users/{self.user_id}/Items"
                async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
                    resp_m = await client.get(
                        url,
                        headers=headers,
                        params={"IncludeItemTypes": "Movie", "Recursive": "true", "Limit": "0"}
                    )
                    resp_s = await client.get(
                        url,
                        headers=headers,
                        params={"IncludeItemTypes": "Series", "Recursive": "true", "Limit": "0"}
                    )
                    if resp_m.status_code == 200 and resp_s.status_code == 200:
                        m_cnt = resp_m.json().get("TotalRecordCount")
                        s_cnt = resp_s.json().get("TotalRecordCount")
                        if m_cnt is not None and s_cnt is not None:
                            return {
                                "movie_count": int(m_cnt),
                                "series_count": int(s_cnt)
                            }
            except Exception as e:
                logger.debug(f"Query /Users/Items count failed: {e}")

        return default_counts

    def get_direct_stream_url(self, item_id: str, media_source_id: Optional[str] = None) -> str:
        """Constructs original direct play stream link (static=true)."""
        base = f"{self.server_url}/Videos/{item_id}/stream"
        query = f"static=true&api_key={self.api_key}"
        if media_source_id:
            query += f"&MediaSourceId={media_source_id}"
        return f"{base}?{query}"

    def get_image_url(self, item_id: str, image_type: str = "Primary", max_width: int = 800) -> str:
        """Constructs Emby image URL."""
        if image_type == "Backdrop":
            return f"{self.server_url}/Items/{item_id}/Images/Backdrop/0?maxWidth={max_width}&api_key={self.api_key}"
        return f"{self.server_url}/Items/{item_id}/Images/{image_type}?maxWidth={max_width}&api_key={self.api_key}"

    # Playback Heartbeat & Reporting
    async def report_playback_start(
        self,
        item_id: str,
        media_source_id: Optional[str] = None,
        position_ticks: int = 0
    ) -> bool:
        """Reports session start: POST /Sessions/Playing."""
        url = f"{self.server_url}/Sessions/Playing"
        payload = {
            "ItemId": item_id,
            "MediaSourceId": media_source_id or item_id,
            "PlayMethod": "DirectPlay",
            "PositionTicks": position_ticks,
            "CanSeek": True,
            "VolumeLevel": 100,
            "IsMuted": False,
            "IsPaused": False,
            "RepeatMode": "RepeatNone"
        }
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            try:
                resp = await client.post(url, json=payload, headers=self._get_headers())
                return resp.status_code in (200, 204)
            except Exception as e:
                logger.error(f"Error reporting playback start: {e}")
                return False

    async def report_playback_progress(
        self,
        item_id: str,
        position_ticks: int,
        is_paused: bool = False,
        event: str = "TimeUpdate",
        media_source_id: Optional[str] = None
    ) -> bool:
        """Reports 10s playback progress heartbeat: POST /Sessions/Playing/Progress."""
        url = f"{self.server_url}/Sessions/Playing/Progress"
        payload = {
            "ItemId": item_id,
            "MediaSourceId": media_source_id or item_id,
            "PositionTicks": position_ticks,
            "IsPaused": is_paused,
            "PlayMethod": "DirectPlay",
            "Event": event
        }
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            try:
                resp = await client.post(url, json=payload, headers=self._get_headers())
                return resp.status_code in (200, 204)
            except Exception as e:
                logger.error(f"Error reporting playback progress: {e}")
                return False

    async def report_playback_stopped(
        self,
        item_id: str,
        position_ticks: int,
        media_source_id: Optional[str] = None
    ) -> bool:
        """Reports playback stopped: POST /Sessions/Playing/Stopped."""
        url = f"{self.server_url}/Sessions/Playing/Stopped"
        payload = {
            "ItemId": item_id,
            "MediaSourceId": media_source_id or item_id,
            "PositionTicks": position_ticks
        }
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            try:
                resp = await client.post(url, json=payload, headers=self._get_headers())
                return resp.status_code in (200, 204)
            except Exception as e:
                logger.error(f"Error reporting playback stopped: {e}")
                return False

    async def mark_played(self, item_id: str) -> bool:
        """Marks item as played: POST /Users/{user_id}/PlayedItems/{item_id}."""
        url = f"{self.server_url}/Users/{self.user_id}/PlayedItems/{item_id}"
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            try:
                resp = await client.post(url, headers=self._get_headers())
                return resp.status_code in (200, 204)
            except Exception as e:
                logger.error(f"Error marking item played: {e}")
                return False

    async def mark_unplayed(self, item_id: str) -> bool:
        """Marks item as unplayed: DELETE /Users/{user_id}/PlayedItems/{item_id}."""
        url = f"{self.server_url}/Users/{self.user_id}/PlayedItems/{item_id}"
        async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
            try:
                resp = await client.delete(url, headers=self._get_headers())
                return resp.status_code in (200, 204)
            except Exception as e:
                logger.error(f"Error marking item unplayed: {e}")
                return False

    def to_onyx_item(self, emby_item: Dict[str, Any], source_id: str) -> Dict[str, Any]:
        """
        Normalizes an Emby/Jellyfin item into OnyxVision unified media schema.
        Extracts 4K/HDR/Atmos tags, technical specs, cast/crew, and ambient color.
        """
        raw_type = emby_item.get("Type", "").lower()
        if raw_type == "movie":
            item_type = "movie"
        elif raw_type in ("series", "show"):
            item_type = "series"
        elif raw_type == "season":
            item_type = "season"
        elif raw_type == "episode":
            item_type = "episode"
        else:
            item_type = "movie"

        item_id = f"emby_{emby_item.get('Id')}"
        title = emby_item.get("Name", "未命名")
        original_title = emby_item.get("OriginalTitle", title)
        year = emby_item.get("ProductionYear") or (emby_item.get("PremiereDate", "")[:4] if emby_item.get("PremiereDate") else None)
        try:
            year = int(year) if year else None
        except Exception:
            year = None

        overview = emby_item.get("Overview", "")
        taglines = emby_item.get("Taglines", [])
        tagline = taglines[0] if taglines else ""

        # Badges and Tech specs parsing
        tags = []
        media_sources = emby_item.get("MediaSources", [])
        tech_info = {}
        stream_url = ""

        if media_sources:
            ms0 = media_sources[0]
            ms_id = ms0.get("Id")
            stream_url = self.get_direct_stream_url(emby_item.get("Id"), ms_id)
            container = ms0.get("Container", "").upper()
            bitrate_bps = ms0.get("Bitrate", 0)
            bitrate_mbps = f"{round(bitrate_bps / 1_000_000, 1)} Mbps" if bitrate_bps else ""

            # Video stream analysis
            streams = ms0.get("MediaStreams", [])
            v_stream = next((s for s in streams if s.get("Type") == "Video"), {})
            a_stream = next((s for s in streams if s.get("Type") == "Audio"), {})

            width = v_stream.get("Width", 0)
            height = v_stream.get("Height", 0)
            v_codec = v_stream.get("Codec", "").upper()
            video_range = (v_stream.get("VideoRange") or v_stream.get("VideoRangeType") or "").upper()
            audio_codec = a_stream.get("Codec", "").upper()
            channels = a_stream.get("Channels", 2)
            audio_profile = a_stream.get("Profile", "")

            # Resolution badge
            if width >= 3800 or height >= 2100:
                tags.append("4K UHD")
            elif width >= 1900 or height >= 1000:
                tags.append("1080p FHD")
            elif width >= 1200 or height >= 700:
                tags.append("720p HD")

            # HDR / Dolby Vision badge
            if "DOVI" in video_range or "VISION" in video_range:
                tags.append("Dolby Vision")
            if "HDR10+" in video_range or "HDR10PLUS" in video_range:
                tags.append("HDR10+")
            elif "HDR" in video_range:
                tags.append("HDR10")

            # Audio badges
            if "ATMOS" in audio_profile.upper() or "ATMOS" in a_stream.get("DisplayTitle", "").upper():
                tags.append("Dolby Atmos")
            elif "TRUEHD" in audio_codec:
                tags.append("Dolby TrueHD")
            elif "DTS" in audio_codec:
                if "MA" in audio_profile.upper() or "MASTER" in audio_profile.upper():
                    tags.append("DTS-HD MA")
                else:
                    tags.append("DTS")
            elif "EAC3" in audio_codec:
                tags.append("Dolby Digital Plus")

            # Codec badge
            if v_codec in ("HEVC", "H265"):
                tags.append("HEVC 10-bit" if v_stream.get("BitDepth") == 10 else "HEVC")
            elif v_codec in ("H264", "AVC"):
                tags.append("H.264")

            tech_info = {
                "resolution": f"{width}x{height}" if width and height else "",
                "video_codec": v_codec,
                "audio_codec": audio_codec,
                "audio_channels": f"{channels} 声道" if channels else "",
                "bitrate": bitrate_mbps,
                "container": container,
                "aspect_ratio": v_stream.get("AspectRatio", ""),
                "fps": f"{round(float(v_stream['RealFrameRate']), 2)} fps" if (v_stream.get("RealFrameRate") and str(v_stream.get("RealFrameRate")).replace('.', '', 1).isdigit()) else (str(v_stream.get("RealFrameRate") or ""))
            }
        else:
            stream_url = self.get_direct_stream_url(emby_item.get("Id"))

        # Actors and Directors
        people = emby_item.get("People", [])
        actors = []
        directors = []
        for p in people:
            p_type = p.get("Type", "")
            p_name = p.get("Name", "")
            p_role = p.get("Role", "")
            p_id = p.get("Id", "")
            p_thumb = self.get_image_url(p_id, "Primary", 200) if p_id else ""
            if p_type in ("Actor", "GuestStar") and len(actors) < 10:
                actors.append({"name": p_name, "role": p_role, "thumb": p_thumb})
            elif p_type == "Director" and len(directors) < 3:
                directors.append(p_name)

        # Poster & Backdrop
        poster = self.get_image_url(emby_item.get("Id"), "Primary", 780)
        backdrop = self.get_image_url(emby_item.get("Id"), "Backdrop", 1920)

        # Dynamic ambient color based on item title hash
        color_palette = ["#1e3a8a", "#b46a2a", "#c2410c", "#047857", "#4338ca", "#7e22ce", "#be123c", "#0f766e"]
        h_val = int(hashlib.md5(title.encode()).hexdigest(), 16)
        ambient_color = color_palette[h_val % len(color_palette)]

        # Duration
        runtime_ticks = emby_item.get("RunTimeTicks", 0)
        duration_sec = int(runtime_ticks / 10_000_000) if runtime_ticks else 0
        cr = emby_item.get("CommunityRating")
        try:
            rating_num = round(float(cr), 1) if cr is not None else 8.0
        except Exception:
            rating_num = 8.0

        return {
            "id": item_id,
            "source_id": source_id,
            "source_item_id": emby_item.get("Id"),
            "type": item_type,
            "title": title,
            "original_title": original_title,
            "year": year,
            "overview": overview,
            "tagline": tagline,
            "poster": poster,
            "backdrop": backdrop,
            "banner": backdrop,
            "logo": "",
            "rating": rating_num,
            "community_rating": rating_num,
            "genres": json.dumps(emby_item.get("Genres", []), ensure_ascii=False),
            "actors": json.dumps(actors, ensure_ascii=False),
            "directors": json.dumps(directors, ensure_ascii=False),
            "duration": duration_sec,
            "release_date": emby_item.get("PremiereDate", "")[:10] if emby_item.get("PremiereDate") else "",
            "ambient_color": ambient_color,
            "tags": json.dumps(tags, ensure_ascii=False),
            "technical_info": json.dumps(tech_info, ensure_ascii=False),
            "stream_url": stream_url,
            "parent_id": f"emby_{emby_item.get('SeriesId')}" if emby_item.get("SeriesId") else None,
            "series_id": f"emby_{emby_item.get('SeriesId')}" if emby_item.get("SeriesId") else None,
            "season_number": emby_item.get("ParentIndexNumber", 0),
            "episode_number": emby_item.get("IndexNumber", 0),
            "is_favorite": 1 if emby_item.get("UserData", {}).get("IsFavorite") else 0
        }

    # Backward compatibility alias
    to_vidhub_item = to_onyx_item
