"""AIOGitHubAPI: AIOGitHubAPI"""
from __future__ import annotations

import os
from typing import List, Optional

import aiohttp

from ..common.const import ACCEPT_HEADERS
from ..objects.base import AIOGitHubAPIBase
from ..objects.repository import AIOGitHubAPIRepository
from .client import AIOGitHubAPIClient


class AIOGitHubAPI(AIOGitHubAPIBase):
    """
    AIOGitHubAPI

    This is the main class this is where it all starts.

    DEPRECATED: Use `GitHubAPI` instead.
    """

    _close_session = False

    def __init__(
        self,
        token: str = None,
        session: aiohttp.ClientSession = None,
        headers: Optional[dict] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Initialises a GitHub API client.

        param | required | description
        -- | -- | --
        `token` | False | [Your GitHub Personal Access Token](https://github.com/settings/tokens).
        `session` | False | `aiohttp.ClientSession` to be used by this package.
        `headers` | False | Custom headers to be used by this package.
        `base_url` | False | Base URL of the GitHub API.

        """
        if session is None:
            session = aiohttp.ClientSession()
            self._close_session = True

        if token is None:
            token = os.getenv("GITHUB_TOKEN")

        self.client = AIOGitHubAPIClient(session, token, headers, base_url)

    async def __aenter__(self) -> "AIOGitHubAPI":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self._close()

    async def get_repo(
        self,
        repo: str,
        etag: Optional[str] = None,
    ) -> AIOGitHubAPIRepository:
        """Retrun AIOGitHubAPIRepository object."""
        _endpoint = f"/repos/{repo}"
        _headers = {"Accept": ACCEPT_HEADERS["preview"]}
        if etag:
            _headers[aiohttp.hdrs.IF_NONE_MATCH] = etag

        response = await self.client.get(endpoint=_endpoint, headers=_headers)

        return AIOGitHubAPIRepository(self.client, response.data)

    async def get_org_repos(
        self, org: str, page: int = 1, etag: Optional[str] = None
    ) -> List[AIOGitHubAPIRepository]:
        """
        Retrun a list of AIOGitHubAPIRepository objects.

        param | required | Default | description
        -- | -- | -- | --
        `org` | True | None | The name of the organization, example "octocat"
        `page` | False | 1 | The page number you want to fetch.
        """
        _enpoint = f"/orgs/{org}/repos?page={str(page)}"
        _params = {"per_page": 100}
        _headers = {"Accept": ACCEPT_HEADERS["preview"]}
        if etag:
            _headers[aiohttp.hdrs.IF_NONE_MATCH] = etag

        response = await self.client.get(endpoint=_enpoint, params=_params, headers=_headers)

        return [AIOGitHubAPIRepository(self.client, x) for x in response.data or []]

    async def graphql(self, query: str, variables: dict = {}) -> dict:
        response = await self.client.post(
            endpoint="/graphql",
            returnjson=True,
            data={"query": query, "variables": variables},
            jsondata=True,
        )
        return response.data.get("data")

    async def get_rate_limit(self) -> dict:
        """Retrun current rate limits."""
        _endpoint = "/rate_limit"

        await self.client.get(endpoint=_endpoint)
        return self.client.ratelimits.__dict__

    async def render_markdown(self, content: str, etag: Optional[str] = None) -> str:
        """
        Retrun AIOGitHubAPIRepository object.

        [API Docs](https://docs.github.com/en/rest/reference/markdown#render-a-markdown-document-in-raw-mode)

        param | description
        -- | --
        `content` | The content (as markdown) you want to render as GHF Markdown
        """
        _endpoint = "/markdown/raw"
        _headers = {"Content-Type": "text/plain"}
        if etag:
            _headers[aiohttp.hdrs.IF_NONE_MATCH] = etag

        response = await self.client.post(endpoint=_endpoint, headers=_headers, data=content)

        return response.data

    async def _close(self) -> None:
        """Close open client session."""
        if self.client.session and self._close_session:
            await self.client.session.close()
