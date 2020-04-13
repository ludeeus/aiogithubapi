"""
AioGitHub: Base

https://github.com/ludeeus/aiogithubapi
"""
# pylint: disable=redefined-builtin, import-outside-toplevel
import logging
from aiogithubapi.client import AioGitHubAPIClient

_LOGGER = logging.getLogger("AioGitHub")


class AIOGitHub:
    """Base Github API implementation."""

    def __init__(self, token, session):
        """Must be called before anything else."""
        self.client = AioGitHubAPIClient(session, token)
        self.token = token
        self.session = session

    async def get_repo(self, repo: str):
        """Retrun AIOGithubRepository object."""
        from aiogithubapi import AIOGithubRepository

        _endpoint = f"/repos/{repo}"
        _headers = {"Accept": "application/vnd.github.mercy-preview+json"}

        response = await self.client.get(endpoint=_endpoint, headers=_headers)

        return AIOGithubRepository(response, self.token, self.session)

    async def get_org_repos(self, org: str, page=1):
        """Retrun a list of AIOGithubRepository objects."""
        from aiogithubapi import AIOGithubRepository

        _enpoint = f"/orgs/{org}/repos?page={str(page)}"
        _params = {"per_page": 100}
        _headers = {"Accept": "application/vnd.github.mercy-preview+json"}

        response = await self.client.get(
            endpoint=_enpoint, params=_params, headers=_headers
        )

        return [
            AIOGithubRepository(x, self.token, self.session) for x in response or []
        ]

    async def render_markdown(self, content: str):
        """Retrun AIOGithubRepository object."""
        _endpoint = "/markdown/raw"
        _headers = {"Content-Type": "text/plain"}

        return await self.client.post(
            endpoint=_endpoint, headers=_headers, data=content
        )

    async def get_ratelimit(self):
        """Retrun current ratelimits."""
        return await self.client.get("/rate_limit")
