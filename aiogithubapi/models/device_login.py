"""GitHub device login data class."""
from __future__ import annotations

from pydantic import BaseModel


class GitHubLoginDeviceModel(BaseModel):
    """GitHub device login data class."""

    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int
