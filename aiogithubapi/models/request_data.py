"""Dataclass to hold base request details."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from aiohttp.hdrs import AUTHORIZATION, USER_AGENT

from ..const import (
    BASE_API_HEADERS,
    BASE_API_URL,
    DEFAULT_USER_AGENT,
    GitHubClientKwarg,
)
from .base import GitHubBase


@dataclass
class GitHubBaseRequestDataModel(GitHubBase):
    """Dataclass to hold base request details."""

    kwargs: Dict[GitHubClientKwarg, Any]
    token: str | None = None

    def __post_init__(self):
        """Check user agent."""
        if self.headers[USER_AGENT] == DEFAULT_USER_AGENT:
            self.logger.debug(
                "User-Agent not set. Set this with passing a user-agent header or the client_name argument."
            )

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
    def headers(self) -> Dict[str, str]:
        """Return base request headers."""
        headers = BASE_API_HEADERS.copy()
        if self.token:
            headers[AUTHORIZATION] = f"token {self.token}"
        if kwarg_headers := self.kwargs.get(GitHubClientKwarg.HEADERS):
            headers.update(kwarg_headers)
        if client_name := self.kwargs.get(GitHubClientKwarg.CLIENT_NAME):
            headers[USER_AGENT] = client_name
        return headers
