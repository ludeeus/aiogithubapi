"""
AIOGitHubAPI: AioGitHubClient

This is the class that do the requests against the API
It also keeps track of ratelimits
"""
# pylint: disable=redefined-builtin, too-many-arguments
from __future__ import annotations

from typing import Optional

import aiohttp

from ..common.const import BASE_API_HEADERS, BASE_API_URL
from ..helpers import async_call_api
from ..objects.base import AIOGitHubAPIBase, AIOGitHubAPIResponse
from ..objects.ratelimit import AIOGitHubAPIRateLimit


class AIOGitHubAPIClient(AIOGitHubAPIBase):
    """
    Client to handle API calls.

    Deprecated: Used by old versions of the library.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: str,
        headers: Optional[dict] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """Initialize the API client."""
        self.session = session
        self.base_url = base_url or BASE_API_URL
        self.last_response: Optional[AIOGitHubAPIResponse] = None
        self.token = token
        self.ratelimits = AIOGitHubAPIRateLimit()
        self.headers = {}
        self.headers.update(BASE_API_HEADERS)
        self.headers.update(headers or {})

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
        url = f"{self.base_url}{endpoint}"
        _headers = {}
        _headers.update(self.headers)
        _headers.update(headers or {})

        response = await async_call_api(
            session=self.session,
            method="GET",
            url=url,
            returnjson=returnjson,
            headers=_headers,
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
        url = f"{self.base_url}{endpoint}"
        _headers = {}
        _headers.update(self.headers)
        _headers.update(headers or {})

        response = await async_call_api(
            session=self.session,
            method="POST",
            url=url,
            returnjson=returnjson,
            headers=_headers,
            params=params,
            data=data,
            jsondata=jsondata,
        )
        self.ratelimits.load_from_response_headers(response.headers)
        self.last_response = response
        return response
