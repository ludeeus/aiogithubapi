"""
Class for OAuth device flow authentication.

https://docs.github.com/en/developers/apps/authorizing-oauth-apps#device-flow
"""
from __future__ import annotations

import asyncio
from datetime import datetime

import aiohttp

from ..common.const import (
    LOGGER,
    OAUTH_ACCESS_TOKEN,
    OAUTH_DEVICE_LOGIN,
    DeviceFlowError,
    HttpMethod,
)
from ..common.exceptions import AIOGitHubAPIException
from ..objects.login.device import AIOGitHubAPILoginDevice
from ..objects.login.oauth import AIOGitHubAPILoginOauth
from .helpers import async_call_api

HEADERS = {"Accept": "application/json"}


class AIOGitHubAPIDeviceLogin:
    _close_session = False

    def __init__(
        self,
        client_id: str,
        scope: str = "",
        session: aiohttp.ClientSession = None,
    ):
        """
        Initialises a GitHub API OAuth device flow.

        param | required | description
        -- | -- | --
        `client_id` | True | The client ID of your OAuth app.
        `scope` | False | [Scope(s)](https://docs.github.com/en/developers/apps/scopes-for-oauth-apps) that will be requested.
        `session` | False | `aiohttp.ClientSession` to be used by this package.
        """
        self.client_id = client_id
        self.scope = scope
        self._interval = 5
        self._expires_in = None
        self._expires = None
        self._device_code = None

        if session is None:
            self.session = aiohttp.ClientSession()
            self._close_session = True
        else:
            self.session = session

    async def __aenter__(self) -> "AIOGitHubAPIDeviceLogin":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self._close()

    async def async_register_device(self) -> AIOGitHubAPILoginDevice:
        """Register the device and return a object that contains the user code for authorization."""
        params = {"client_id": self.client_id, "scope": self.scope}
        response = await async_call_api(
            session=self.session,
            method=HttpMethod.POST,
            url=OAUTH_DEVICE_LOGIN,
            params=params,
            headers=HEADERS,
        )
        device = AIOGitHubAPILoginDevice(response.data)
        self._device_code = device.device_code
        self._interval = device.interval
        self._expires = datetime.timestamp(datetime.now()) + device.expires_in

        return device

    async def async_device_activation(self) -> AIOGitHubAPILoginOauth:
        """Wait for the user to enter the code and activate the device."""
        _activation = None
        while _activation is None:
            if self._expires is None or self._device_code is None:
                await asyncio.sleep(self._interval)

            params = {
                "client_id": self.client_id,
                "device_code": self._device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            }

            if self._expires < datetime.timestamp(datetime.now()):
                raise AIOGitHubAPIException("User took too long to enter key")

            try:
                response = await async_call_api(
                    session=self.session,
                    method=HttpMethod.POST,
                    url=OAUTH_ACCESS_TOKEN,
                    params=params,
                    headers=HEADERS,
                )
                if response.data.get("error"):
                    if response.data["error"] == DeviceFlowError.AUTHORIZATION_PENDING:
                        LOGGER.debug(response.data["error_description"])
                        await asyncio.sleep(self._interval)
                    else:
                        raise AIOGitHubAPIException(response.data["error_description"])
                else:
                    _activation = AIOGitHubAPILoginOauth(response.data)
                    break

            except AIOGitHubAPIException as exception:
                raise AIOGitHubAPIException(exception) from exception

        return _activation

    async def _close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()
