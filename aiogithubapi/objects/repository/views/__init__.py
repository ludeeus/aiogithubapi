"""
AIOGitHubAPI: Clones

https://docs.github.com/en/rest/reference/repos#get-repository-clones
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

    async def get(self,) -> dict:
        """Gets views traffic."""
        _endpoint = f"/repos/{self.repository.full_name}/traffic/views"

        return await self.client.get(endpoint=_endpoint)
