"""
AIOGitHubAPI: Repository Traffic

https://docs.github.com/en/rest/reference/repos#traffic
"""
from datetime import datetime

from aiogithubapi.objects.base import AIOGitHubAPIBaseClient
from aiogithubapi.objects.repos.traffic.clones import AIOGitHubAPIReposTrafficClones
from aiogithubapi.objects.repos.traffic.pageviews import (
    AIOGitHubAPIReposTrafficPageviews,
)


class AIOGitHubAPIRepositoryTraffic(AIOGitHubAPIBaseClient):
    """Repository Release GitHub API implementation."""

    @property
    def full_name(self) -> None:
        return self.attributes.get("full_name")

    async def get_views(self):
        _endpoint = f"/repos/{self.full_name}/traffic/views"
        response = await self.client.get(endpoint=_endpoint)
        return AIOGitHubAPIReposTrafficPageviews(response.data)

    async def get_clones(self) -> None:
        _endpoint = f"/repos/{self.full_name}/traffic/clones"
        response = await self.client.get(endpoint=_endpoint)
        return AIOGitHubAPIReposTrafficClones(response.data)
