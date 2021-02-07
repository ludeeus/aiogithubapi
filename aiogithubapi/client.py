"""
AIOGitHubAPI: AioGitHubClient

This is the class that do the requests against the API
It also keeps track of ratelimits
"""
# pylint: disable=redefined-builtin, too-many-arguments
from typing import Optional
import aiohttp

from aiogithubapi.common.const import BASE_API_HEADERS, BASE_API_URL
from aiogithubapi.helpers import async_call_api
from aiogithubapi.objects.base import AIOGitHubAPIBase, AIOGitHubAPIResponse
from aiogithubapi.objects.ratelimit import AIOGitHubAPIRateLimit


class AIOGitHubAPIClient(AIOGitHubAPIBase):
    """Client to handle API calls."""

    def __init__(self, session: aiohttp.ClientSession, token: str) -> None:
        """Initialize the API client."""
        self.session = session
        self.last_response: Optional[AIOGitHubAPIResponse] = None
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
    ) -> AIOGitHubAPIResponse:
        """Execute a GET request."""
        url = f"{BASE_API_URL}{endpoint}"
        response = await async_call_api(
            session=self.session,
            method="GET",
            url=url,
            returnjson=returnjson,
            headers=headers,
            params=params,
        )
        self.ratelimits.load_from_response_headers(response.headers)
        self.last_response = response
        return response

    async def post(
        self,
        endpoint: str,
        returnjson: bool = False,
        headers: dict or None = None,
        params: dict or None = None,
        data: dict or str or None = None,
        jsondata: bool = False,
    ) -> AIOGitHubAPIResponse:
        """Execute a POST request."""
        url = f"{BASE_API_URL}{endpoint}"
        response = await async_call_api(
            session=self.session,
            method="POST",
            url=url,
            returnjson=returnjson,
            headers=headers,
            params=params,
            data=data,
            jsondata=jsondata,
        )
        self.ratelimits.load_from_response_headers(response.headers)
        self.last_response = response
        return response
