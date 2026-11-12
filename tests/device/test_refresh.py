"""Test expiring device credentials and token rotation."""

import asyncio
from unittest.mock import patch

import pytest

from aiogithubapi import (
    GitHubAPI,
    GitHubAuthenticationException,
    GitHubConnectionException,
    GitHubDeviceAPI,
    GitHubException,
    GitHubLoginOauthModel,
    GitHubRatelimitException,
)
from tests.common import CLIENT_ID, DEVICE_CODE, MockedRequests, MockResponse

TOKENS = {
    "access_token": "new-access",
    "refresh_token": "new-refresh",
    "expires_in": 28800,
    "refresh_token_expires_in": 15897600,
    "token_type": "bearer",
}


@pytest.mark.asyncio
async def test_refresh(
    github_device_api: GitHubDeviceAPI, mock_response: MockResponse, mock_requests: MockedRequests
):
    mock_response.mock_data = TOKENS
    with patch("aiogithubapi.device.time.time", return_value=1000):
        response = await github_device_api.refresh("old-refresh")
    assert response.data.access_token == "new-access"
    assert response.data.refresh_token == "new-refresh"
    assert response.data.expires_at == 29800
    assert response.data.refresh_token_expires_at == 15898600
    assert mock_requests.last_request["json"] == {
        "client_id": CLIENT_ID,
        "refresh_token": "old-refresh",
        "grant_type": "refresh_token",
    }
    assert "params" not in mock_requests.last_request
    assert mock_requests.last_request["allow_redirects"] is False
    assert "Authorization" not in mock_requests.last_request["headers"]


@pytest.mark.asyncio
async def test_activation_preserves_refresh_fields(
    github_device_api: GitHubDeviceAPI, mock_response: MockResponse
):
    mock_response.mock_data = TOKENS
    with patch("aiogithubapi.device.time.time", return_value=1000):
        response = await github_device_api.activation(DEVICE_CODE)
    assert response.data.refresh_token == "new-refresh"
    assert response.data.expires_at == 29800


@pytest.mark.parametrize("status", [200, 400, 401])
@pytest.mark.parametrize("code", ["bad_refresh_token", "invalid_grant"])
@pytest.mark.asyncio
async def test_rejected_refresh(
    github_device_api: GitHubDeviceAPI, mock_response: MockResponse, status: int, code: str
):
    mock_response.mock_status = status
    mock_response.mock_data = {"error": code, "error_description": "private-response"}
    with pytest.raises(GitHubAuthenticationException, match="invalid or expired"):
        await github_device_api.refresh("old-refresh")


@pytest.mark.parametrize(
    ("status", "code", "exception"),
    [
        (503, "invalid_grant", GitHubConnectionException),
        (429, "invalid_grant", GitHubRatelimitException),
        (200, "incorrect_client_credentials", GitHubException),
    ],
)
@pytest.mark.asyncio
async def test_nonterminal_failure(
    github_device_api: GitHubDeviceAPI,
    mock_response: MockResponse,
    status: int,
    code: str,
    exception: type[GitHubException],
):
    mock_response.mock_status = status
    mock_response.mock_data = {"error": code, "error_description": "private-response"}
    with pytest.raises(exception) as raised:
        await github_device_api.refresh("old-refresh")
    assert not isinstance(raised.value, GitHubAuthenticationException)
    assert "private-response" not in str(raised.value)


@pytest.mark.asyncio
async def test_omitted_refresh_token(
    github_device_api: GitHubDeviceAPI, mock_response: MockResponse
):
    mock_response.mock_data = {"access_token": "new-access", "expires_in": 3600}
    response = await github_device_api.refresh("old-refresh")
    assert response.data.refresh_token == "old-refresh"
    assert response.data.refresh_token_expires_at is None


@pytest.mark.asyncio
async def test_cancellation_propagates(
    github_device_api: GitHubDeviceAPI, mock_response: MockResponse
):
    mock_response.mock_raises = asyncio.CancelledError()
    with pytest.raises(asyncio.CancelledError):
        await github_device_api.refresh("old-refresh")


@pytest.mark.parametrize(
    "data",
    [
        {**TOKENS, "access_token": ""},
        {**TOKENS, "expires_in": None},
        {**TOKENS, "expires_in": -1},
        {**TOKENS, "refresh_token_expires_in": "86400"},
    ],
)
def test_invalid_token_data(data: dict):
    with pytest.raises(GitHubException):
        GitHubLoginOauthModel(data)


@pytest.mark.asyncio
async def test_set_token_preserves_contents_accept_header(
    github_api: GitHubAPI, mock_response: MockResponse, mock_requests: MockedRequests
):
    contents = github_api.repos.contents
    mock_response.mock_data = {"type": "file", "content": "e30=", "encoding": "base64"}
    github_api.set_token("new-access")
    await contents.get("octocat/hello-world", "hacs.json")
    assert mock_requests.last_request["headers"]["Authorization"] == "token new-access"
    assert mock_requests.last_request["headers"]["Accept"] == "application/vnd.github.v3+json"
