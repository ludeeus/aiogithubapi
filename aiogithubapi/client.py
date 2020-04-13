"""AioGitHub: AioGitHubClient"""
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
from aiogithubapi.ratelimit import RateLimitResources, AIOGithubRateLimits

_LOGGER = logging.getLogger("AioGitHub")


class AioGitHubAPIClient:
    """Client to handle API calls."""

    def __init__(self, session, token):
        """Initialize the client."""
        self.session = session
        self.token = token
        self.ratelimits = RateLimitResources()
        self.headers = BASE_HEADERS
        self.headers["Authorization"] = "token {}".format(token)

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def get(self, endpoint, returnjson=True, headers=None):
        """Execute a GET request."""
        _url = f"{BASE_URL}{endpoint}"
        _headers = self.headers
        for header in headers or []:
            _headers[header] = headers[header]

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.get(_url, headers=_headers)
            self.ratelimits.load_from_response_headers(response.headers)

            if response.status is RATELIMIT_HTTP_CODE:
                raise AIOGitHubRatelimit("GitHub Ratelimit error")

            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(
                    f"GitHub returned {response.status} for {_url}"
                )

            if returnjson:
                response = await response.json()
                if response.get("message"):
                    if response["message"] == "Bad credentials":
                        raise AIOGitHubAuthentication("Access token is not valid!")
                    raise AIOGitHubException(response["message"])
            else:
                response = await response.text()
                if isinstance(response, dict):
                    if response.get("message"):
                        if response["message"] == "Bad credentials":
                            raise AIOGitHubAuthentication("Access token is not valid!")
                        raise AIOGitHubException(response["message"])
        return response

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def post(self, endpoint, headers=None, data=None):
        """Execute a POST request."""
