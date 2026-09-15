from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SourceCreateRequest(BaseModel):
    name: str = Field(..., description="Display name for the media source")
    type: str = Field(..., description="Source type: emby, jellyfin, webdav, local")
    url: Optional[str] = Field(None, description="Server URL or local path")
    username: Optional[str] = Field(None, description="Username for authentication")
    password: Optional[str] = Field(None, description="Password for authentication")
    api_key: Optional[str] = Field(None, description="API Key or token")
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional options")

class EmbyConnectRequest(BaseModel):
    server_url: str = Field(..., description="Emby / Jellyfin server URL e.g. http://192.168.1.100:8096")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")
    api_key: Optional[str] = Field(None, description="API Key (optional if using user/pass)")
    name: Optional[str] = Field(None, description="Custom display name")

class EmbySyncRequest(BaseModel):
    source_id: str = Field(..., description="Mounted source ID to sync items from")
    view_ids: Optional[List[str]] = Field(None, description="Optional list of library view IDs to sync")

class PlaybackProgressRequest(BaseModel):
    item_id: str = Field(..., description="ID of the media item being played")
    position_seconds: float = Field(..., description="Current playback position in seconds")
    duration_seconds: Optional[float] = Field(0.0, description="Total duration of media in seconds (optional)")
    is_paused: bool = Field(False, description="Whether playback is currently paused")
    event: Optional[str] = Field("TimeUpdate", description="Event name: TimeUpdate, Pause, Unpause, Stopped")

class MarkPlayedRequest(BaseModel):
    item_id: str = Field(..., description="ID of the media item")
    is_played: bool = Field(True, description="True for played, False for unplayed")

class ScanDirectoryRequest(BaseModel):
    directory_path: str = Field(..., description="Local directory path to scan for media files")
    source_id: Optional[str] = Field(None, description="Target source ID")
