"""Helpers for AIOGitHubAPI."""
import logging
from asyncio import CancelledError, TimeoutError, get_event_loop
from typing import Optional

import aiohttp
import async_timeout
import backoff
from aiohttp.client_exceptions import ClientError

from aiogithubapi.common.const import (
    BASE_API_HEADERS,
    HTTP_STATUS_CODE_GOOD_LIST,
    HttpMethod,
    HttpStatusCode,
)
from aiogithubapi.common.exceptions import (
    AIOGitHubAPIAuthenticationException,
    AIOGitHubAPIException,
    AIOGitHubAPIRatelimitException,
)
from aiogithubapi.objects.base import AIOGitHubAPIResponse

_LOGGER: logging.Logger = logging.getLogger("aiogithubapi")


def short_sha(sha: str) -> str:
    return sha[0:7]


def short_message(message: str) -> str:
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
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    data: dict or str or None = None,
    jsondata: bool = True,
    returnjson: bool = True,
) -> AIOGitHubAPIResponse:
    """Execute the API call."""
    _headers = BASE_API_HEADERS
    for header in headers or {}:
        _headers[header] = headers[header]

    response = AIOGitHubAPIResponse()

    async with async_timeout.timeout(20, loop=get_event_loop()):
        if method == HttpMethod.GET:
            result = await session.get(url, params=params or {}, headers=_headers)
        else:
            if jsondata:
                result = await session.post(
                    url,
                    params=params or {},
                    headers=_headers,
                    json=data or {},
                )
            else:
                result = await session.post(
                    url,
                    params=params or {},
                    headers=_headers,
                    data=data or "",
                )

        _LOGGER.debug(result.headers)
        response.status = result.status
        response.headers = result.headers

        if response.status == HttpStatusCode.RATELIMIT:
            raise AIOGitHubAPIRatelimitException("GitHub Ratelimit error")

        elif response.status == HttpStatusCode.UNAUTHORIZED:
            raise AIOGitHubAPIAuthenticationException(HttpStatusCode.UNAUTHORIZED)

        elif response.status not in HTTP_STATUS_CODE_GOOD_LIST:
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
                    raise AIOGitHubAPIAuthenticationException(
                        "Access token is not valid!"
                    )
                raise AIOGitHubAPIException(response.data)

    _LOGGER.debug(response.as_dict())
    return response
