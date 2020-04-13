"""
AioGitHub: Base

https://github.com/ludeeus/aiogithubapi
"""
# pylint: disable=redefined-builtin
import logging
from asyncio import CancelledError, TimeoutError, get_event_loop

import async_timeout
from aiohttp import ClientError

import backoff

from aiogithubapi import (
    BASE_HEADERS,
    BASE_URL,
    GOOD_HTTP_CODES,
    RATELIMIT_HTTP_CODE,
    AIOGitHubAuthentication,
    AIOGitHubException,
    AIOGitHubRatelimit,
)
from aiogithubapi.client import AioGitHubAPIClient
from aiogithubapi.ratelimit import RateLimitResources, AIOGithubRateLimits

_LOGGER = logging.getLogger("AioGitHub")


class AIOGitHub:
    """Base Github API implementation."""

    def __init__(self, token, session):
        """Must be called before anything else."""
        self.client = AioGitHubAPIClient(session, token)
        self.token = token
        self.session = session
        # Only track the "core" ratelimits here, use `get_ratelimit` for full info
        self.ratelimits = RateLimitResources()
        self.headers = BASE_HEADERS
        self.headers["Authorization"] = "token {}".format(token)

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def get_repo(self, repo: str):
        """Retrun AIOGithubRepository object."""
        from aiogithubapi import AIOGithubRepository

        url = f"{BASE_URL}/repos/{repo}"

        headers = self.headers
        headers["Accept"] = "application/vnd.github.mercy-preview+json"

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.get(url, headers=headers)
            self.ratelimits.load_from_resp(response.headers)

            if response.status is RATELIMIT_HTTP_CODE:
                raise AIOGitHubRatelimit("GitHub Ratelimit error")

            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")
            response = await response.json()

            if response.get("message"):
                if response["message"] == "Bad credentials":
                    raise AIOGitHubAuthentication("Access token is not valid!")
                else:
                    raise AIOGitHubException(response["message"])

        return AIOGithubRepository(response, self.token, self.session)

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def get_org_repos(self, org: str, page=1):
        """Retrun a list of AIOGithubRepository objects."""
        from aiogithubapi import AIOGithubRepository

        url = f"{BASE_URL}/orgs/{org}/repos?page={str(page)}"
        params = {"per_page": 100}
        headers = self.headers
        headers["Accept"] = "application/vnd.github.mercy-preview+json"

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.get(url, headers=headers, params=params)
            self.ratelimits.load_from_resp(response.headers)

            if response.status is RATELIMIT_HTTP_CODE:
                raise AIOGitHubRatelimit("GitHub Ratelimit error")
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")

            response = await response.json()

            if not isinstance(response, list):
                if response["message"] == "Bad credentials":
                    raise AIOGitHubAuthentication("Access token is not valid!")
                else:
                    raise AIOGitHubException(response["message"])

            repositories = []

            for repository in response:
                repositories.append(
                    AIOGithubRepository(repository, self.token, self.session)
                )

        return repositories

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def render_markdown(self, content: str):
        """Retrun AIOGithubRepository object."""
        url = f"{BASE_URL}/markdown/raw"
        headers = self.headers
        headers["Content-Type"] = "text/plain"

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.post(url, headers=headers, data=content)
            self.ratelimits.load_from_resp(response.headers)

            if response.status is RATELIMIT_HTTP_CODE:
                raise AIOGitHubRatelimit("GitHub Ratelimit error")
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")
            response = await response.text()

            if isinstance(response, dict):
                if response.get("message"):
                    if response["message"] == "Bad credentials":
                        raise AIOGitHubAuthentication("Access token is not valid!")
                    else:
                        raise AIOGitHubException(response["message"])

        return response

    async def get_ratelimit(self):
        """Retrun current ratelimits."""
        return await self.client.get("/rate_limit")
