"""GitHub login oauth data class."""

from __future__ import annotations

import time
from typing import Any

from ..exceptions import GitHubException
from .base import GitHubDataModelBase


class GitHubLoginOauthModel(GitHubDataModelBase):
    """GitHub login oauth data class."""

    access_token: str | None = None
    token_type: str | None = None
    scope: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    refresh_token_expires_in: int | None = None
    expires_at: float | None = None
    refresh_token_expires_at: float | None = None

    def __init__(self, data: dict[str, Any], *, requested_at: float | None = None) -> None:
        """Parse credentials and anchor lifetimes before the token request."""
        super().__init__(data)
        if not isinstance(self.access_token, str) or not self.access_token:
            raise GitHubException("Invalid OAuth access token response")
        if self.refresh_token is not None and (
            not isinstance(self.refresh_token, str) or not self.refresh_token
        ):
            raise GitHubException("Invalid OAuth refresh token response")
        issued_at = time.time() if requested_at is None else requested_at
        for field, expires_at in (
            ("expires_in", "expires_at"),
            ("refresh_token_expires_in", "refresh_token_expires_at"),
        ):
            lifetime = getattr(self, field)
            if lifetime is None:
                continue
            if type(lifetime) is not int or lifetime <= 0:
                raise GitHubException("Invalid OAuth token lifetime")
            setattr(self, expires_at, issued_at + lifetime)
        if self.refresh_token is not None and self.expires_in is None:
            raise GitHubException("Missing OAuth access token lifetime")
