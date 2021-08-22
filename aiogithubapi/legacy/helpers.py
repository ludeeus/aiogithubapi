"""Helpers for AIOGitHubAPI."""
from asyncio import CancelledError, TimeoutError, get_event_loop
from typing import Optional

import aiohttp
from aiohttp.client_exceptions import ClientError
import async_timeout
import backoff

from ..common.const import HTTP_STATUS_CODE_GOOD_LIST, HttpMethod, HttpStatusCode
from ..common.exceptions import (
    AIOGitHubAPIAuthenticationException,
    AIOGitHubAPIException,
    AIOGitHubAPINotModifiedException,
    AIOGitHubAPIRatelimitException,
)
from ..objects.base import AIOGitHubAPIResponse


def short_sha(sha: str) -> str:
    """Return the first 7 characters of the sha."""
    return sha[0:7]


def short_message(message: str) -> str:
    """Return the first line of a message"""
    return message.split("\n")[0]


@backoff.on_exception(
    backoff.expo,
    (ClientError, CancelledError, TimeoutError, KeyError),
    max_tries=5,
    logger=None,
)
async def async_call_api(
    session: aiohttp.ClientSession,
    method: HttpMethod,
    url: str,
    headers: dict,
    params: Optional[dict] = None,
    data: dict or str or None = None,
    jsondata: bool = True,
    returnjson: bool = True,
) -> AIOGitHubAPIResponse:
    """Execute the API call."""
    response = AIOGitHubAPIResponse()

    async with async_timeout.timeout(20, loop=get_event_loop()):
        if method == HttpMethod.GET:
            result = await session.get(url, params=params or {}, headers=headers)
        else:
            if jsondata:
                result = await session.post(
                    url,
                    params=params or {},
                    headers=headers,
                    json=data or {},
                )
            else:
                result = await session.post(
                    url,
                    params=params or {},
                    headers=headers,
                    data=data or "",
                )

        response.status = result.status
        response.headers = result.headers

        if response.status == HttpStatusCode.RATELIMIT:
            raise AIOGitHubAPIRatelimitException("GitHub Ratelimit error")

        if response.status == HttpStatusCode.UNAUTHORIZED:
            raise AIOGitHubAPIAuthenticationException(HttpStatusCode.UNAUTHORIZED)

        if response.status == HttpStatusCode.NOT_MODIFIED:
            raise AIOGitHubAPINotModifiedException(f"Response from {url} was not modified.")

        if response.status not in HTTP_STATUS_CODE_GOOD_LIST:
            raise AIOGitHubAPIException(
                f"GitHub returned {HttpStatusCode(response.status)} for {url}"
            )

        if returnjson:
            response.data = await result.json()
        else:
            response.data = await result.text()

        if isinstance(response.data, dict):
            if response.data.get("message"):
                if response.data["message"] == "Bad credentials":
                    raise AIOGitHubAPIAuthenticationException("Access token is not valid!")
                raise AIOGitHubAPIException(response.data)

    return response
