"""AIOGitHubAPI: objects.base"""
from aiogithubapi.common.const import HttpStatusCode
import logging


class AIOGitHubAPIBase:
    """Base class for AIOGitHubAPI."""

    logger: logging.Logger = logging.getLogger("AIOGitHubAPI")

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
        self.headers = {}
        self.status = HttpStatusCode.OK
        self.data = None

    def as_dict(self):
        """Return attributes as a dict."""
        return {"headers": self.headers, "status": self.status, "data": self.data}
