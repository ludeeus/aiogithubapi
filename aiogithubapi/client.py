"""This is the class that do the requests against the API."""
from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

from .const import (
    GitHubClientKwarg,
    GitHubRequestKwarg,
    HttpContentType,
    HttpMethod,
    HttpStatusCode,
)
from .exceptions import (
    GitHubAuthenticationException,
    GitHubConnectionException,
    GitHubException,
    GitHubNotModifiedException,
    GitHubRatelimitException,
)
from .legacy.client import AIOGitHubAPIClient as LegacyAIOGitHubAPIClient
from .models import GitHubBase, GitHubBaseRequestDataModel, GitHubResponseModel

STATUS_EXCEPTIONS: dict[HttpStatusCode, GitHubException] = {
    HttpStatusCode.RATELIMIT: GitHubRatelimitException,
    HttpStatusCode.UNAUTHORIZED: GitHubAuthenticationException,
    HttpStatusCode.NOT_MODIFIED: GitHubNotModifiedException,
}


class AIOGitHubAPIClient(LegacyAIOGitHubAPIClient):
    """Dummy class to not break existing code."""


class GitHubClient(GitHubBase):
    """
    Client to handle API calls.

    Don't use this directly, use `aiogithubapi.github.GitHubApi` to get the client.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: str | None = None,
        **kwargs: dict[GitHubClientKwarg, Any],
    ) -> None:
        """Initialise the GitHub API client."""
        self._base_request_data = GitHubBaseRequestDataModel(
            token=token,
            kwargs=kwargs,
        )
        self._session = session

    async def async_call_api(
        self,
        endpoint: str,
        *,
        data: dict[str, Any] | str | None = None,
        **kwargs: dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel:
        """Execute the API call."""
        request_arguments: dict[str, Any] = {
            "url": self._base_request_data.request_url(endpoint),
            "method": kwargs.get(GitHubRequestKwarg.METHOD, HttpMethod.GET).lower(),
            "params": kwargs.get(GitHubRequestKwarg.PARAMS)
            or kwargs.get(GitHubRequestKwarg.QUERY, {}),
            "timeout": self._base_request_data.timeout,
            "headers": {
                **self._base_request_data.headers,
                **kwargs.get("headers", {}),
            },
        }

        if etag := kwargs.get(GitHubRequestKwarg.ETAG):
            request_arguments["headers"][aiohttp.hdrs.IF_NONE_MATCH] = etag

        if isinstance(data, dict):
            request_arguments["json"] = data
        else:
            request_arguments["data"] = data

        try:
            result = await self._session.request(**request_arguments)
        except (aiohttp.ClientError, asyncio.CancelledError) as exception:
            raise GitHubConnectionException(
                "Request exception for "
                f"'{self._base_request_data.request_url(endpoint)}' with - {exception}"
            ) from exception

        except asyncio.TimeoutError:
            raise GitHubConnectionException(
                f"Timeout of {self._base_request_data.timeout} reached while "
                f"waiting for {self._base_request_data.request_url(endpoint)}"
            ) from None

        except BaseException as exception:
            raise GitHubException(
                "Unexpected exception for "
                f"'{self._base_request_data.request_url(endpoint)}' with - {exception}"
            ) from exception

        response = GitHubResponseModel(result)

        if response.status != HttpStatusCode.NO_CONTENT:
            if response.headers.content_type != HttpContentType.TEXT_PLAIN:
                response.data = await result.json()
                if (
                    response.status == HttpStatusCode.RATELIMIT
                    and "rate limit" not in str(response.data).lower()
                ):
                    response.status = HttpStatusCode.UNAUTHORIZED
            else:
                response.data = await result.text()

            if exception := STATUS_EXCEPTIONS.get(response.status):
                raise exception(response.data)

        if isinstance(response.data, dict):
            if message := response.data.get("message"):
                if message == "Bad credentials":
                    raise GitHubAuthenticationException("Access token is not valid!")
                raise GitHubException(response.data)

        return response
