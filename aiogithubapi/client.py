"""AIOGitHubAPI: AioGitHubClient"""
# pylint: disable=redefined-builtin, too-many-arguments
from asyncio import CancelledError, TimeoutError, get_event_loop
from aiohttp import ClientError

import async_timeout
import backoff

from aiogithubapi.common.exceptions import (
    AIOGitHubAPIAuthenticationException,
    AIOGitHubAPIException,
    AIOGitHubAPIRatelimitException,
)
from aiogithubapi.common.const import (
    BASE_API_HEADERS,
    BASE_API_URL,
    HTTP_STATUS_CODE_GOOD_LIST,
    HTTP_STATUS_CODE_RATELIMIT,
)
from aiogithubapi.objects.base import AIOGitHubAPIBase
from aiogithubapi.objects.ratelimit import AIOGitHubAPIRateLimit


class AIOGitHubAPIClient(AIOGitHubAPIBase):
    """Client to handle API calls."""

    def __init__(self, session: "aiohttp.ClientSession", token: str) -> None:
        """Initialize the client."""
        self.session = session
        self.token = token
        self.ratelimits = AIOGitHubAPIRateLimit()
        self.headers = BASE_API_HEADERS
        if token is not None:
            self.headers["Authorization"] = "token {}".format(token)

    async def get(
        self,
        endpoint: str,
        returnjson: bool = True,
        headers: dict or None = None,
        params: dict or None = None,
    ):
        """Execute a GET request."""
        return await self.call_api("GET", endpoint, returnjson, headers, params)

    async def post(
        self,
        endpoint: str,
        returnjson: bool = False,
        headers: dict or None = None,
        params: dict or None = None,
        data: dict or str or None = None,
        jsondata: bool = False,
    ):
        """Execute a POST request."""
        return await self.call_api(
            "POST", endpoint, returnjson, headers, params, data, jsondata
        )

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def call_api(
        self,
        call: str in ["GET", "POST"],
        endpoint: str,
        returnjson: bool,
        headers: dict,
        params: dict,
        data: dict or None = None,
        jsondata: bool = False,
    ):
        """Execute the API call."""
        _url = f"{BASE_API_URL}{endpoint}"
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
            self.logger.debug(response.headers)
            self.ratelimits.load_from_response_headers(response.headers)

            if response.status == HTTP_STATUS_CODE_RATELIMIT:
                raise AIOGitHubAPIRatelimitException("GitHub Ratelimit error")

            if response.status not in HTTP_STATUS_CODE_GOOD_LIST:
                raise AIOGitHubAPIException(
                    f"GitHub returned {response.status} for {_url}"
                )

            if returnjson:
                response = await response.json()
            else:
                response = await response.text()

            if isinstance(response, dict):
                if response.get("message"):
                    if response["message"] == "Bad credentials":
                        raise AIOGitHubAPIAuthenticationException(
                            "Access token is not valid!"
                        )
                    raise AIOGitHubAPIException(response["message"])

        self.logger.debug(response)
        return response
