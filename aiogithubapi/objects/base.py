"""AIOGitHubAPI: objects.base"""
import logging


class AIOGitHubAPIBase:
    """Base class for AIOGitHubAPI."""

    logger = logging.getLogger("AIOGitHubAPI")

    def __init__(self, attributes) -> None:
        """Initialize."""
        self.attributes = attributes


class AIOGitHubAPIBaseClient(AIOGitHubAPIBase):
    """Base class for AIOGitHubAPI."""

    def __init__(self, client: "AIOGitHubAPIClient", attributes: dict) -> None:
        """Initialise."""
        super().__init__(attributes)
        self.client = client
