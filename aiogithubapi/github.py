"""AIOGitHubAPI: AIOGitHubAPI"""
from aiohttp import ClientSession

from aiogithubapi.objects import (
    AIOGitHubAPIBase,
    AIOGitHubAPIRepository,
)

from aiogithubapi.client import AIOGitHubAPIClient

from aiogithubapi.common.const import ACCEPT_HEADERS


class AIOGitHubAPI(AIOGitHubAPIBase):
    """
    AIOGitHubAPI

    This is the main class this is where it all starts.
    """

    def __init__(self, session: type(ClientSession), token: str) -> None:
        """
        Initialises a GitHub API client.

        :param token:       Your GitHub Personal Access Token
                            https://github.com/settings/tokens
        :param session:     aiohttp.ClientSession to be used by this package.
        """
        self.client = AIOGitHubAPIClient(session, token)
        self.session = session
        self.token = token

    async def get_repo(self, repo: str) -> type(AIOGitHubAPIRepository):
        """Retrun AIOGitHubAPIRepository object."""
        _endpoint = f"/repos/{repo}"
        _headers = {"Accept": ACCEPT_HEADERS["preview"]}

        response = await self.client.get(endpoint=_endpoint, headers=_headers)

        return AIOGitHubAPIRepository(self.client, response)

    async def get_org_repos(
        self, org: str, page: int = 1
    ) -> [type(AIOGitHubAPIRepository)]:
        """
        Retrun a list of AIOGitHubAPIRepository objects.

        :param org:         The name of the organization
                            Example: "octocat"
        :param page:        The page number you want to fetch
                            Default: 1
        """
        _enpoint = f"/orgs/{org}/repos?page={str(page)}"
        _params = {"per_page": 100}
        _headers = {"Accept": ACCEPT_HEADERS["preview"]}

        response = await self.client.get(
            endpoint=_enpoint, params=_params, headers=_headers
        )

        return [AIOGitHubAPIRepository(self.client, x) for x in response or []]

    async def render_markdown(self, content: str) -> str:
        """
        Retrun AIOGitHubAPIRepository object.

        :param content:     The content (as markdown) you want to render
        """
        _endpoint = "/markdown/raw"
        _headers = {"Content-Type": "text/plain"}

        return await self.client.post(
            endpoint=_endpoint, headers=_headers, data=content
        )

    async def get_ratelimit(self) -> dict:
        """Retrun current ratelimits."""
        return await self.client.get("/rate_limit")
