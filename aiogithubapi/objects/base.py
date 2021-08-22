"""AIOGitHubAPI: objects.base"""
from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.hdrs import ETAG

from ..common.const import HttpStatusCode

if TYPE_CHECKING:
    from ..client import AIOGitHubAPIClient


class AIOGitHubAPIBase:
    """Base class for AIOGitHubAPI."""

    def __init__(self, attributes) -> None:
        """Initialize."""
        self.attributes = attributes


class AIOGitHubAPIBaseClient(AIOGitHubAPIBase):
    """Base class for AIOGitHubAPI."""

    def __init__(self, client: AIOGitHubAPIClient, attributes: dict) -> None:
        """Initialise."""
        super().__init__(attributes)
        self.client = client


class AIOGitHubAPIResponse:
    """Response object for AIOGitHub."""

    def __init__(self) -> None:
        """initialise."""
        self.headers: dict = {}
        self.data = {}
        self.status: HttpStatusCode = HttpStatusCode.OK

    def as_dict(self):
        """Return attributes as a dict."""
        return {
            "headers": self.headers,
            "status": self.status,
            "data": self.data,
            "etag": self.etag,
        }

    @property
    def etag(self):
        """Return the ETag for this response."""
        return self.headers.get(ETAG)
