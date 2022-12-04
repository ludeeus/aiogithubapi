"""This is the class that do the requests against the API."""
from __future__ import annotations

import asyncio
from typing import Any, Dict

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
    GitHubGraphQLException,
    GitHubNotFoundException,
    GitHubNotModifiedException,
    GitHubPayloadException,
    GitHubPermissionException,
    GitHubRatelimitException,
)
from .legacy.client import AIOGitHubAPIClient as LegacyAIOGitHubAPIClient
from .models.base import GitHubBase
from .models.request_data import GitHubBaseRequestDataModel
from .models.response import GitHubResponseModel

STATUS_EXCEPTIONS: Dict[HttpStatusCode, GitHubException] = {
    HttpStatusCode.FORBIDDEN: GitHubAuthenticationException,
    HttpStatusCode.UNAUTHORIZED: GitHubAuthenticationException,
    HttpStatusCode.NOT_MODIFIED: GitHubNotModifiedException,
    HttpStatusCode.NOT_FOUND: GitHubNotFoundException,
    HttpStatusCode.BAD_REQUEST: GitHubPayloadException,
    HttpStatusCode.UNPROCESSABLE_ENTITY: GitHubException,
}

MESSAGE_EXCEPTIONS: Dict[str, GitHubException] = {
    "Bad credentials": GitHubAuthenticationException,
    "You have exceeded a secondary rate limit and have been temporarily blocked from content creation. Please retry your request again later.": GitHubRatelimitException,
    "Must have push access to repository": GitHubPermissionException,
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
        *,
        api_version: str | None = None,
        **kwargs: Dict[GitHubClientKwarg, Any],
    ) -> None:
        """
        Initialise the GitHub API client.

        **Arguments:**
        `session`: The aiohttp client session to use for making requests.
        `token`: The GitHub access token to use for authenticating requests. Can be a string or None.
        `api_version`: The version of the GitHub API to use. Can be a string or None.

        """
        self._base_request_data = GitHubBaseRequestDataModel(
            token=token,
            api_version=api_version,
            kwargs=kwargs,
        )
        self._session = session
        self._loop = asyncio.get_running_loop()

    async def async_call_api(
        self,
        endpoint: str,
        *,
        data: Dict[str, Any] | str | None = None,
        headers: Dict[str, Any] | None = None,
        method: HttpMethod = HttpMethod.GET,
        params: Dict[str, Any] | None = None,
        timeout: int | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel:
        """
        Makes an HTTP request to the specified endpoint using the specified parameters.

        This method is asynchronous, meaning that it will not block the execution of the program while the request is being made and processed.

        **Arguments**:

        -  `endpoint` (Required): The API endpoint to call.

        **Optional arguments**:
        - `endpoint`: The API endpoint to call.
        - `data`: The data to include in the request body. Can be a dictionary, a string, or None.
        - `headers`: The headers to include in the request. Can be a dictionary or None.
        - `method`: The HTTP method to use for the request. Defaults to GET.
        - `params`: The query parameters to include in the request. Can be a dictionary or None.
        - `timeout`: The maximum amount of time to wait for the request to complete, in seconds. Can be an integer or None.

        Returns:
        A GitHubResponseModel object representing the API response.
        """
        request_arguments: Dict[str, Any] = {
            "url": self._base_request_data.request_url(endpoint),
            "method": kwargs.get(GitHubRequestKwarg.METHOD, method).lower(),
            "params": params
            or kwargs.get(GitHubRequestKwarg.PARAMS, kwargs.get(GitHubRequestKwarg.QUERY, {})),
            "timeout": timeout or self._base_request_data.timeout,
            "headers": {
                **self._base_request_data.headers,
                **(headers or {}),
                **kwargs.get("headers", {}),
            },
        }

        print(request_arguments["headers"])

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
        if response.status == HttpStatusCode.NO_CONTENT:
            return response

        try:
            if HttpContentType.BASE_JSON in (response.headers.content_type or ""):
                response.data = await result.json(encoding="utf-8")
            elif (response.headers.content_type or "") in (
                HttpContentType.BASE_ZIP,
                HttpContentType.BASE_GZIP,
            ):
                response.data = await result.read()
            else:
                response.data = await result.text(encoding="utf-8")
        except BaseException as exception:
            raise GitHubException(
                f"Could not handle response data from '{self._base_request_data.request_url(endpoint)}' with - {exception}"
            )
        message = response.data.get("message") if isinstance(response.data, dict) else None

        if message is not None and "rate limit" in message:
            raise GitHubRatelimitException(message)

        if exception := STATUS_EXCEPTIONS.get(response.status):
            raise exception(message or response.data)

        if isinstance(response.data, dict):
            if message is not None:
                if exception := MESSAGE_EXCEPTIONS.get(message):
                    raise exception(message)
                raise GitHubException(message)

        if endpoint == "/graphql" and response.data.get("errors", []):
            raise GitHubGraphQLException(
                ", ".join(entry.get("message") for entry in response.data["errors"])
            )

        return response
