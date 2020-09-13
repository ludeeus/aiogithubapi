"""
Class for OAuth device flow authentication.

https://docs.github.com/en/developers/apps/authorizing-oauth-apps#device-flow
"""
import asyncio
import logging
from datetime import datetime

import aiohttp

from aiogithubapi.common.const import (
    OAUTH_ACCESS_TOKEN,
    OAUTH_DEVICE_LOGIN,
    DeviceFlowError,
    HttpMethod,
)
from aiogithubapi.common.exceptions import AIOGitHubAPIException
from aiogithubapi.helpers import async_call_api
from aiogithubapi.objects.login.device import AIOGitHubAPILoginDevice
from aiogithubapi.objects.login.oauth import AIOGitHubAPILoginOauth

_LOGGER: logging.Logger = logging.getLogger("aiogithubapi")

HEADERS = {"Accept": "application/json"}


class AIOGitHubAPIDeviceLogin:
    _close_session = False

    def __init__(
        self, client_id: str, scope: str = "", session: aiohttp.ClientSession = None
    ):
        """
        Initialises a GitHub API OAuth device flow.

        :param client_id:   The client ID of your OAuth app.
        :param scope:       Scope(s) that will be requested.
        :param session:     aiohttp.ClientSession to be used by this package.
        """
        self.client_id = client_id
        self.scope = scope
        self._interval = None
        self._expires_in = None

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
        await self.close()

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

    async def async_device_activation(self) -> AIOGitHubAPILoginOauth or None:
        """Wait for the user to enter the code and activate the device."""
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
                    _LOGGER.debug(response.data["error_description"])
                    await asyncio.sleep(self._interval)
                    await self.async_device_activation()
                else:
                    raise AIOGitHubAPIException(response.data["error_description"])
            else:
                return AIOGitHubAPILoginOauth(response.data)

        except AIOGitHubAPIException as exception:
            raise AIOGitHubAPIException(exception)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()
