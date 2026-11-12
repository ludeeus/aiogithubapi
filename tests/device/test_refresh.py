"""Test expiring device credentials and token rotation."""

import asyncio
import json
from unittest.mock import patch

from aiohttp import ClientSession
from aresponses import ResponsesMockServer
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


@pytest.mark.parametrize("header_name", ["Authorization", "authorization", "AUTHORIZATION"])
@pytest.mark.parametrize("token", ["new-access", None, ""])
@pytest.mark.asyncio
async def test_set_token_replaces_configured_authorization(
    client_session: ClientSession,
    mock_response: MockResponse,
    mock_requests: MockedRequests,
    header_name: str,
    token: str | None,
):
    headers = {header_name: "token old-access", "X-Custom": "preserved"}
    api = GitHubAPI(token="initial-access", session=client_session, headers=headers)
    contents = api.repos.contents
    mock_response.mock_data = {"type": "file", "content": "e30=", "encoding": "base64"}

    api.set_token(token)
    await contents.get("octocat/hello-world", "hacs.json")

    sent = mock_requests.last_request["headers"]
    authorization = [value for name, value in sent.items() if name.lower() == "authorization"]
    assert authorization == ([f"token {token}"] if token else [])
    assert sent["X-Custom"] == "preserved"
    assert sent["Accept"] == "application/vnd.github.v3+json"
    assert headers == {header_name: "token old-access", "X-Custom": "preserved"}


@pytest.mark.parametrize(
    ("status", "code", "exception"),
    [
        (400, "bad_refresh_token", GitHubAuthenticationException),
        (401, "invalid_grant", GitHubAuthenticationException),
        (429, "invalid_grant", GitHubRatelimitException),
        (503, "invalid_grant", GitHubConnectionException),
    ],
)
@pytest.mark.asyncio
async def test_refresh_classifies_errors_with_automatic_status_raising(
    aresponses: ResponsesMockServer,
    status: int,
    code: str,
    exception: type[GitHubException],
):
    aresponses.add(
        "github.com",
        "/login/oauth/access_token",
        "post",
        aresponses.Response(
            status=status,
            text=json.dumps({"error": code}),
            headers={"Content-Type": "application/json"},
        ),
    )
    async with ClientSession(raise_for_status=True) as session:
        device = GitHubDeviceAPI(CLIENT_ID, session=session)
        with pytest.raises(exception) as raised:
            await device.refresh("old-refresh")
        assert type(raised.value) is exception
    aresponses.assert_plan_strictly_followed()
