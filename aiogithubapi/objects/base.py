"""AIOGitHubAPI: objects.base"""
import logging

from aiogithubapi.common.const import HttpStatusCode


class AIOGitHubAPIBase:
    """Base class for AIOGitHubAPI."""

    logger: logging.Logger = logging.getLogger("aiogithubapi")

    def __init__(self, attributes) -> None:
        """Initialize."""
        self.attributes = attributes


class AIOGitHubAPIBaseClient(AIOGitHubAPIBase):
    """Base class for AIOGitHubAPI."""

    def __init__(self, client: "AIOGitHubAPIClient", attributes: dict) -> None:
        """Initialise."""
        super().__init__(attributes)
        self.client = client


class AIOGitHubAPIResponse:
    """Response object for AIOGitHub."""

    def __init__(self) -> None:
        """initialise."""
        self.headers: dict = {}
        self.status: HttpStatusCode = HttpStatusCode.OK
        self.data: dict or str = {}

    def as_dict(self):
        """Return attributes as a dict."""
        return {"headers": self.headers, "status": self.status, "data": self.data}
