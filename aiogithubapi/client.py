"""AioGitHub: AioGitHubClient"""
# pylint: disable=redefined-builtin, too-many-arguments
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
from aiogithubapi.ratelimit import RateLimitResources

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

    async def get(self, endpoint, returnjson=True, headers=None, params=None):
        """Execute a GET request."""
        return await self.call_api("GET", endpoint, returnjson, headers, params)

    async def post(
        self,
        endpoint,
        returnjson=False,
        headers=None,
        params=None,
        data=None,
        jsondata=False,
    ):
        """Execute a POST request."""
        return await self.call_api(
            "POST", endpoint, returnjson, headers, params, data, jsondata
        )

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def call_api(
        self, call, endpoint, returnjson, headers, params, data=None, jsondata=False
    ):
        """Execute the API call."""
        _url = f"{BASE_URL}{endpoint}"
        _headers = self.headers
        _params = {}

        for header in headers or []:
            _headers[header] = headers[header]

        for param in params or []:
            _params[param] = params[param]

        async with async_timeout.timeout(20, loop=get_event_loop()):
            if call == "GET":
                response = await self.session.get(
                    _url, params=_params, headers=_headers
                )
            else:
                if jsondata:
                    response = await self.session.post(
                        _url, params=_params, headers=_headers, json=data
                    )
                else:
                    response = await self.session.post(
                        _url, params=_params, headers=_headers, data=data
                    )
            _LOGGER.debug(response.headers)
            self.ratelimits.load_from_response_headers(response.headers)

            if response.status is RATELIMIT_HTTP_CODE:
                raise AIOGitHubRatelimit("GitHub Ratelimit error")

            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(
                    f"GitHub returned {response.status} for {_url}"
                )

            if returnjson:
                response = await response.json()
            else:
                response = await response.text()

            if isinstance(response, dict):
                if response.get("message"):
                    if response["message"] == "Bad credentials":
                        raise AIOGitHubAuthentication("Access token is not valid!")
                    raise AIOGitHubException(response["message"])

        _LOGGER.debug(response)
        return response
