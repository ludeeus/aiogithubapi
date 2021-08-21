"""GitHub device login data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class GitHubLoginDeviceModel(GitHubDataModelBase):
    """GitHub device login data class."""

    device_code: str | None = None
    user_code: str | None = None
    verification_uri: str | None = None
    expires_in: int | None = None
    interval: int | None = None
