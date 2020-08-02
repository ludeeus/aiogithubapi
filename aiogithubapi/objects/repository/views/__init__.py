"""
AIOGitHubAPI: Views

https://docs.github.com/en/rest/reference/repos#get-page-views
"""
# pylint: disable=missing-docstring, unused-import
from aiogithubapi.objects.base import AIOGitHubAPIBase


class AIOGitHubAPIRepositoryViews(AIOGitHubAPIBase):
    """Views traffic GitHub API implementation."""

    def __init__(self, client: "AIOGitHubAPIClient", attributes: dict):
        """Initialize."""
        self.client = client
        self.attributes = attributes

    @property
    def count(self):
        return self.attributes.get("count")

    @property
    def uniques(self):
        return self.attributes.get("uniques")

    async def get(self, repository: str) -> dict:
        """Gets views traffic."""
        _endpoint = f"/repos/{repository}/traffic/views"

        return await self.client.get(endpoint=_endpoint)
