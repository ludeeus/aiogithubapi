"""
Class for OAuth device flow authentication.

https://docs.github.com/en/developers/apps/authorizing-oauth-apps#device-flow
"""

from __future__ import annotations

import asyncio
from datetime import datetime
import time
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
from .exceptions import (
    GitHubAuthenticationException,
    GitHubConnectionException,
    GitHubException,
    GitHubRatelimitException,
)
from .helpers import random_float
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
        self.__interval = 5
        self._expires = None

        if session is None:
            session = aiohttp.ClientSession()
            self._close_session = True

        self._session = session

        if GitHubClientKwarg.BASE_URL not in kwargs:
            kwargs[GitHubClientKwarg.BASE_URL] = BASE_GITHUB_URL

        self._client = GitHubClient(session=session, **kwargs)
        self._token_url = (
            f"{kwargs[GitHubClientKwarg.BASE_URL].rstrip('/')}{OAUTH_ACCESS_TOKEN_PATH}"
        )

    @property
    def _interval(self) -> int | None:
        """Polling interval in seconds; always None or a positive int."""
        return self.__interval

    @_interval.setter
    def _interval(self, value: int | float | None) -> None:
        if isinstance(value, bool):
            self.__interval = None
        elif isinstance(value, int) and value > 0:
            self.__interval = value
        elif isinstance(value, float) and value.is_integer() and value > 0:
            self.__interval = int(value)
        else:
            self.__interval = None

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
        """Register the device and return an object that contains the user code for authorization."""
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

            requested_at = time.time()
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

            if (
                isinstance(response.data, str)
                and "You have exceeded a secondary rate limit" in response.data
            ):
                raise GitHubAuthenticationException(
                    "Secondary rate limit exceeded, try again in 1 hour"
                )

            if error := response.data.get("error"):
                if error in (DeviceFlowError.AUTHORIZATION_PENDING, DeviceFlowError.SLOW_DOWN):
                    if interval := response.data.get("interval"):
                        self._interval = interval
                        if (validated_interval := self._interval) is not None:
                            self.logger.info(
                                "Got new interval instruction of %s from the API",
                                validated_interval,
                            )
                    wait = self._interval or 5
                    sleep_seconds = wait + random_float(wait * 0.1, wait)
                    self.logger.debug(
                        "%s, waiting %.2f seconds before retrying",
                        response.data.get("error_description"),
                        sleep_seconds,
                    )
                    await asyncio.sleep(sleep_seconds)
                else:
                    self.logger.debug(response.data.get("error_description"))
                    raise GitHubException(response.data.get("error_description"))
            else:
                response.data = GitHubLoginOauthModel(response.data, requested_at=requested_at)
                break

        return response

    async def refresh(self, refresh_token: str) -> GitHubResponseModel[GitHubLoginOauthModel]:
        """Renew a device-flow token, returning the rotated credentials.

        A rejected refresh token raises GitHubAuthenticationException. Temporary,
        malformed, and client-configuration failures preserve the caller's login
        by raising other GitHubException subclasses.
        """
        requested_at = time.time()
        try:
            async with self._session.post(
                self._token_url,
                json={
                    "client_id": self.client_id,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
                headers={
                    **{
                        name: value
                        for name, value in self._client._base_request_data.headers.items()
                        if name.lower() not in ("authorization", "accept", "content-type")
                    },
                    "Accept": "application/json",
                },
                timeout=aiohttp.ClientTimeout(total=self._client._base_request_data.timeout),
                allow_redirects=False,
                raise_for_status=False,
            ) as result:
                response = GitHubResponseModel(result)
                if result.status == 429:
                    raise GitHubRatelimitException("GitHub OAuth token endpoint rate limited")
                if result.status >= 500:
                    raise GitHubConnectionException("GitHub OAuth token endpoint unavailable")
                payload = await result.json()
        except (aiohttp.ClientError, TimeoutError, ValueError) as exception:
            raise GitHubConnectionException("GitHub OAuth token refresh failed") from exception

        if not isinstance(payload, dict):
            raise GitHubException("Invalid OAuth token refresh response")
        if payload.get("error") in ("bad_refresh_token", "invalid_grant"):
            raise GitHubAuthenticationException("GitHub refresh token is invalid or expired")
        if response.status != 200 or payload.get("error"):
            raise GitHubException("GitHub OAuth token refresh was refused")
        if "refresh_token" not in payload:
            payload = {**payload, "refresh_token": refresh_token}
        elif payload["refresh_token"] is None:
            raise GitHubException("Invalid OAuth refresh token response")
        response.data = GitHubLoginOauthModel(payload, requested_at=requested_at)
        return response
