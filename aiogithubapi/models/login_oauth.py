"""GitHub login oauth data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class GitHubLoginOauthModel(GitHubDataModelBase):
    """GitHub login oauth data class."""

    access_token: str | None = None
    token_type: str | None = None
    scope: str | None = None
