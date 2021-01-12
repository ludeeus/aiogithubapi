"""
AIOGitHubAPI: AioGitHubClient

This is the class that do the requests against the API
It also keeps track of ratelimits
"""
# pylint: disable=redefined-builtin, too-many-arguments
import aiohttp

from aiogithubapi.common.const import (
    ATTR_DATA,
    BASE_API_HEADERS,
    BASE_API_URL,
    ATTR_ETAG,
    HttpStatusCode,
)
from aiogithubapi.helpers import async_call_api
from aiogithubapi.objects.base import AIOGitHubAPIBase, AIOGitHubAPIResponse
from aiogithubapi.objects.ratelimit import AIOGitHubAPIRateLimit


class AIOGitHubAPIClient(AIOGitHubAPIBase):
    """Client to handle API calls."""

    def __init__(self, session: aiohttp.ClientSession, token: str) -> None:
        """Initialize the API client."""
        self._cache = {}
        self.session = session
        self.token = token
        self.ratelimits = AIOGitHubAPIRateLimit()
        self.headers = BASE_API_HEADERS
        if token is not None:
            self.headers["Authorization"] = f"token {token}"

    async def get(
        self,
        endpoint: str,
        returnjson: bool = True,
        headers: dict or None = None,
        params: dict or None = None,
    ) -> AIOGitHubAPIResponse:
        """Execute a GET request."""
        url = f"{BASE_API_URL}{endpoint}"
        if self._cache.get(endpoint, {}).get(ATTR_ETAG):
            headers["If-None-Match"] = self._cache[endpoint][ATTR_ETAG]
        response = await async_call_api(
            session=self.session,
            method="GET",
            url=url,
            returnjson=returnjson,
            headers=headers,
            params=params,
        )

        self.ratelimits.load_from_response_headers(response.headers)
        if endpoint in self._cache and response.status == HttpStatusCode.NOT_MODIFIED:
            return self._cache[endpoint][ATTR_DATA]
        self._cache[endpoint] = {
            ATTR_ETAG: response.headers.get(ATTR_ETAG),
            ATTR_DATA: response.data,
        }
        return response.data

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
        return response.data
