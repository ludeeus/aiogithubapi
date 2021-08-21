"""Used for the GitHub API namespace."""
from ..client import GitHubClient


class BaseNamespace:
    """Used for the GitHub API namespace."""

    def __init__(self, client: GitHubClient) -> None:
        """Initialise the namespace."""
        self._client = client
        self.__post_init__()

    def __post_init__(self) -> None:
        """Post initialisation."""
