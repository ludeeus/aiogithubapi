"""Construction tests for the device object."""
# pylint: disable=protected-access,missing-function-docstring
from __future__ import annotations

import aiohttp
import pytest

from aiogithubapi import GitHubClientKwarg, GitHubDeviceAPI

from tests.common import CLIENT_ID


@pytest.mark.asyncio
async def test_session_creation():
    device = GitHubDeviceAPI(client_id=CLIENT_ID)
    assert device._session
    assert isinstance(device._session, aiohttp.ClientSession)

    assert not device._session.closed
    await device.close_session()
    assert device._session.closed


@pytest.mark.asyncio
async def test_session_pass():
    async with aiohttp.ClientSession() as session:
        device = GitHubDeviceAPI(client_id=CLIENT_ID, session=session)
        assert device._session is session


@pytest.mark.asyncio
async def test_session_creation_with_enter():
    async with GitHubDeviceAPI(client_id=CLIENT_ID) as device:
        assert device._session
        assert isinstance(device._session, aiohttp.ClientSession)
        assert not device._session.closed

    assert device._session.closed


@pytest.mark.asyncio
async def test_interval_validation():
    device = GitHubDeviceAPI(client_id=CLIENT_ID)
    assert device._interval == 5  # __init__ default
    for bad in (0, -5, None, "x", True, False, 20.5, -1.0):
        device._interval = bad
        assert device._interval is None
    device._interval = 12
    assert device._interval == 12
    device._interval = 20.0  # integer-valued float coerced to int
    assert device._interval == 20
    assert isinstance(device._interval, int)
    await device.close_session()


@pytest.mark.asyncio
async def test_base_url():
    async with GitHubDeviceAPI(client_id=CLIENT_ID) as device:
        assert device._client._base_request_data.base_url == "https://github.com"

    async with GitHubDeviceAPI(
        client_id=CLIENT_ID, **{GitHubClientKwarg.BASE_URL: "https://example.com"}
    ) as device:
        assert device._client._base_request_data.base_url == "https://example.com"
