"""
Class for OAuth device flow authentication.

https://docs.github.com/en/developers/apps/authorizing-oauth-apps#device-flow
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict

import aiohttp

from .client import GitHubClient
from .const import (
    BASE_GITHUB_URL,
    OAUTH_ACCESS_TOKEN_PATH,
    OAUTH_DEVICE_LOGIN_PATH,
    DeviceFlowError,
    GitHubClientKwarg,
    GitHubRequestKwarg,
    HttpMethod,
)
from .exceptions import GitHubException
from .legacy.device import AIOGitHubAPIDeviceLogin as LegacyAIOGitHubAPIDeviceLogin
from .models.base import GitHubBase
from .models.device_login import GitHubLoginDeviceModel
from .models.login_oauth import GitHubLoginOauthModel
from .models.response import GitHubResponseModel


class AIOGitHubAPIDeviceLogin(LegacyAIOGitHubAPIDeviceLogin):
    """Dummy class to not break existing code."""


class GitHubDeviceAPI(GitHubBase):
    """GitHub API OAuth device flow"""

    _close_session = False

    def __init__(
        self,
        client_id: str,
        session: aiohttp.ClientSession | None = None,
        **kwargs: Dict[GitHubClientKwarg, Any],
    ):
        """
        Initialises a GitHub API OAuth device flow.

        **Arguments**:

        `client_id` (Optional)

        The client ID of your OAuth app.


        `session` (Optional)

        `aiohttp.ClientSession` to be used by this package.
        If you do not pass one, one will be created for you.

        `**kwargs` (Optional)

        Pass additional arguments.
        See the `aiogithubapi.const.GitHubClientKwarg` enum for valid options.

        https://docs.github.com/en/developers/apps/authorizing-oauth-apps#device-flow
        """
        self.client_id = client_id
        self._interval = 5
        self._expires = None

        if session is None:
            session = aiohttp.ClientSession()
            self._close_session = True

        self._session = session

        if GitHubClientKwarg.BASE_URL not in kwargs:
            kwargs[GitHubClientKwarg.BASE_URL] = BASE_GITHUB_URL

        self._client = GitHubClient(session=session, **kwargs)

    async def __aenter__(self) -> GitHubDeviceAPI:
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close_session()

    async def close_session(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def register(
        self,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubLoginDeviceModel]:
        """Register the device and return a object that contains the user code for authorization."""
        response = await self._client.async_call_api(
            endpoint=OAUTH_DEVICE_LOGIN_PATH,
            **{
                **kwargs,
                GitHubRequestKwarg.METHOD: HttpMethod.POST,
                GitHubRequestKwarg.PARAMS: {
                    "client_id": self.client_id,
                    "scope": kwargs.get(GitHubRequestKwarg.SCOPE, ""),
                },
            },
        )
        response.data = GitHubLoginDeviceModel(response.data)
        self._interval = response.data.interval
        self._expires = datetime.timestamp(datetime.now()) + response.data.expires_in
        return response

    async def activation(
        self,
        device_code: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubLoginOauthModel]:
        """
        Wait for the user to enter the code and activate the device.

        **Arguments**:

        `device_code`

        The device_code that was returned when registering the device.

        """
        if self._expires is None:
            raise GitHubException("Expiration has passed, re-run the registration")

        _user_confirmed = None
        while _user_confirmed is None:

            if self._expires < datetime.timestamp(datetime.now()):
                raise GitHubException("User took too long to enter key")

            response = await self._client.async_call_api(
                endpoint=OAUTH_ACCESS_TOKEN_PATH,
                **{
                    **kwargs,
                    GitHubRequestKwarg.METHOD: HttpMethod.POST,
                    GitHubRequestKwarg.PARAMS: {
                        "client_id": self.client_id,
                        "device_code": device_code,
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    },
                },
            )

            if error := response.data.get("error"):
                if error == DeviceFlowError.AUTHORIZATION_PENDING:
                    self.logger.debug(response.data.get("error_description"))
                    await asyncio.sleep(self._interval)
                else:
                    raise GitHubException(response.data.get("error_description"))
            else:
                response.data = GitHubLoginOauthModel(response.data)
                break

        return response
