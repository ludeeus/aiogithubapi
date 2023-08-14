"""Test device_flow."""
# pylint: disable=missing-docstring,protected-access
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from aiogithubapi import (
    DeviceFlowError,
    GitHubDeviceAPI,
    GitHubException,
    GitHubRequestKwarg,
)

from tests.common import CLIENT_ID, DEVICE_CODE, TOKEN, MockedRequests, MockResponse


@pytest.mark.asyncio
async def test_register_device(
    github_device_api: GitHubDeviceAPI,
    mock_requests: MockedRequests,
):
    response = await github_device_api.register()
    assert response.status == 200
    assert response.data.verification_uri == "https://github.com/login/device"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://github.com/login/device/code"
    assert mock_requests.last_request["params"]["scope"] == ""
    assert mock_requests.last_request["params"]["client_id"] == CLIENT_ID


@pytest.mark.asyncio
async def test_register_device_custom_scope(
    github_device_api: GitHubDeviceAPI,
    mock_requests: MockedRequests,
):
    response = await github_device_api.register(**{GitHubRequestKwarg.SCOPE: "custom"})
    assert response.status == 200
    assert response.data.verification_uri == "https://github.com/login/device"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://github.com/login/device/code"
    assert mock_requests.last_request["params"]["scope"] == "custom"


@pytest.mark.asyncio
async def test_device_activation(
    github_device_api: GitHubDeviceAPI,
    mock_requests: MockedRequests,
):
    response = await github_device_api.activation(device_code=DEVICE_CODE)
    assert response.status == 200
    assert response.data.access_token == TOKEN
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://github.com/login/oauth/access_token"


@pytest.mark.asyncio
async def test_missing_expiration(github_device_api: GitHubDeviceAPI):
    github_device_api._expires = None
    with pytest.raises(GitHubException, match="Expiration has passed, re-run the registration"):
        await github_device_api.activation(device_code=DEVICE_CODE)


@pytest.mark.asyncio
async def test_user_too_slow(github_device_api: GitHubDeviceAPI):
    github_device_api._expires = datetime.timestamp(datetime.now()) - 1
    with pytest.raises(GitHubException, match="User took too long to enter key"):
        await github_device_api.activation(device_code=DEVICE_CODE)


@pytest.mark.asyncio
async def test_wait_for_confirmation(
    github_device_api: GitHubDeviceAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
    caplog: pytest.CaptureFixture,
    asyncio_sleep: AsyncMock,
):
    mock_response.mock_data_list = [
        {
            "error": DeviceFlowError.AUTHORIZATION_PENDING,
            "error_description": "Pending user authorization",
        },
        {
            "error": DeviceFlowError.AUTHORIZATION_PENDING,
            "error_description": "Pending user authorization",
        },
        {
            "error": DeviceFlowError.SLOW_DOWN,
            "error_description": "Too many requests have been made in the same timeframe.",
            "interval": 20
        },
        {
            "error": DeviceFlowError.AUTHORIZATION_PENDING,
            "error_description": "Pending user authorization",
        },
        {
            "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "token_type": "bearer",
            "scope": "user",
        },
    ]
    response = await github_device_api.activation(device_code=DEVICE_CODE)
    assert response.status == 200
    assert mock_requests.called == 5
    assert asyncio_sleep.call_count == 4

    # Use default interval
    assert asyncio_sleep.call_args_list[-3][0][0] == 1
    # Use new interval from API
    assert asyncio_sleep.call_args_list[-2][0][0] == 20
    # Use default interval
    assert asyncio_sleep.call_args_list[-1][0][0] == 1

    assert mock_requests.last_request["url"] == "https://github.com/login/oauth/access_token"
    assert "Pending user authorization" in caplog.text
    assert "Got new interval instruction of 20 from the API" in caplog.text


@pytest.mark.asyncio
async def test_error_while_waiting(
    github_device_api: GitHubDeviceAPI,
    mock_response: MockResponse,
):
    mock_response.mock_data = {"error": "any",
                               "error_description": "Any error message"}
    with pytest.raises(GitHubException, match="Any error message"):
        await github_device_api.activation(device_code=DEVICE_CODE)
