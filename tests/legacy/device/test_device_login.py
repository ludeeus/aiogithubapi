from datetime import datetime
from unittest.mock import AsyncMock

import aiohttp
import pytest

from aiogithubapi import AIOGitHubAPIException, GitHubDevice, GitHubDeviceAPI

from tests.common import CLIENT_ID, load_fixture
from tests.conftest import client_session


@pytest.mark.asyncio
async def test_session():
    async with aiohttp.ClientSession() as session:
        device = GitHubDevice("xxxxx", "", session)
        assert device.session == session

    async with GitHubDevice("xxxxx") as github:
        assert github.session is not None


@pytest.mark.asyncio
async def test_device(mock_response, github_device: GitHubDevice, asyncio_sleep: AsyncMock):
    device = await github_device.async_register_device()
    assert device.user_code == "WDJB-MJHT"

    mock_response.mock_data_list = [
        {
            "error": "authorization_pending",
            "error_description": "Pending user authorization",
        },
        {
            "access_token": "e72e16c7e42f292c6912e7710c838347ae178b4a",
            "token_type": "bearer",
            "scope": "user",
        },
    ]

    activation = await github_device.async_device_activation()
    assert asyncio_sleep.call_count == 1
    assert asyncio_sleep.call_args[0][0] == 1
    assert activation.access_token == "e72e16c7e42f292c6912e7710c838347ae178b4a"


@pytest.mark.asyncio
async def test_no_user_response(github_device: GitHubDevice):
    device = await github_device.async_register_device()
    assert device.user_code == "WDJB-MJHT"

    with pytest.raises(AIOGitHubAPIException, match="User took too long to enter key"):
        github_device._expires = datetime.timestamp(datetime.now())
        await github_device.async_device_activation()


@pytest.mark.asyncio
async def test_device_error(mock_response, github_device: GitHubDevice):
    device = await github_device.async_register_device()
    assert device.user_code == "WDJB-MJHT"

    mock_response.mock_data = load_fixture("oauth_access_token_error.json", True)

    with pytest.raises(AIOGitHubAPIException, match="Unsupported grant type"):
        await github_device.async_device_activation()


@pytest.mark.asyncio
async def test_no_device_code(github_device: GitHubDevice, asyncio_sleep: AsyncMock):
    with pytest.raises(AIOGitHubAPIException, match="User took too long to enter key"):
        github_device._expires = datetime.timestamp(datetime.now())
        await github_device.async_device_activation()
        assert asyncio_sleep.call_count == 1
        assert asyncio_sleep.call_args[0][0] == 5
