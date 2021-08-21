"""
AIOGitHubAPI: Repository Traffic

https://docs.github.com/en/rest/reference/repos#traffic
"""
from typing import Optional

from aiohttp.hdrs import IF_NONE_MATCH

from ..base import AIOGitHubAPIBaseClient
from ..repos.traffic.clones import AIOGitHubAPIReposTrafficClones
from ..repos.traffic.pageviews import AIOGitHubAPIReposTrafficPageviews


class AIOGitHubAPIRepositoryTraffic(AIOGitHubAPIBaseClient):
    """Repository Release GitHub API implementation."""

    @property
    def full_name(self) -> None:
        return self.attributes.get("full_name")

    async def get_views(self, etag: Optional[str] = None):
        _endpoint = f"/repos/{self.full_name}/traffic/views"
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag
        response = await self.client.get(endpoint=_endpoint, headers=_headers)
        return AIOGitHubAPIReposTrafficPageviews(response.data)

    async def get_clones(self, etag: Optional[str] = None) -> None:
        _endpoint = f"/repos/{self.full_name}/traffic/clones"
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag
        response = await self.client.get(endpoint=_endpoint, headers=_headers)
        return AIOGitHubAPIReposTrafficClones(response.data)
