"""Dataclass to hold base request details."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp.hdrs import AUTHORIZATION

from ..const import BASE_API_HEADERS, BASE_API_URL, GitHubClientKwarg


@dataclass
class GitHubBaseRequestDataModel:
    """Dataclass to hold base request details."""

    kwargs: dict[GitHubClientKwarg, Any]
    token: str | None = None

    def request_url(self, endpoint: str) -> str:
        """Generate full request url."""
        return f"{self.base_url}{endpoint}"

    @property
    def timeout(self) -> int:
        """Return timeout."""
        return self.kwargs.get(GitHubClientKwarg.TIMEOUT) or 20

    @property
    def base_url(self) -> str:
        """Return the base url."""
        return self.kwargs.get(GitHubClientKwarg.BASE_URL) or BASE_API_URL

    @property
    def headers(self) -> dict[str, str]:
        """Return base request headers."""
        headers = BASE_API_HEADERS.copy()
        if self.token:
            headers[AUTHORIZATION] = f"token {self.token}"
        if kwarg_headers := self.kwargs.get(GitHubClientKwarg.HEADERS):
            headers.update(kwarg_headers)
        return headers
