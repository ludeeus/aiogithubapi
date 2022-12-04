"""Test client construction"""
# pylint: disable=missing-docstring,protected-access
from aiohttp import ClientSession
import pytest

from aiogithubapi.client import GitHubClient
from aiogithubapi.const import BASE_API_HEADERS, DEFAULT_USER_AGENT, HEADER_GITHUB_API_VERSION, GitHubClientKwarg

from tests.common import TOKEN


@pytest.mark.asyncio
async def test_client_constrution_defaults(
    client_session: ClientSession, caplog: pytest.CaptureFixture
):
    client = GitHubClient(session=client_session)
    base_request_data = client._base_request_data

    assert client._session == client_session
    assert base_request_data.base_url == "https://api.github.com"
    assert base_request_data.timeout == 20
    assert base_request_data.token is None
    assert base_request_data.kwargs == {}
    assert base_request_data.headers == BASE_API_HEADERS
    assert "Authorization" not in base_request_data.headers
    assert base_request_data.headers["User-Agent"] == DEFAULT_USER_AGENT
    assert (
        "User-Agent not set. Set this with passing a user-agent header or the client_name argument."
        in caplog.text
    )


@pytest.mark.asyncio
async def test_client_constrution_with_token(client_session: ClientSession):
    client = GitHubClient(session=client_session, token=TOKEN)
    base_request_data = client._base_request_data
    assert base_request_data.token == TOKEN
    assert base_request_data.headers == {
        **BASE_API_HEADERS,
        "Authorization": "token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    }


@pytest.mark.asyncio
async def test_client_constrution_with_api_version(client_session: ClientSession):
    client = GitHubClient(session=client_session, token=TOKEN, api_version="3000-01-01")
    base_request_data = client._base_request_data
    assert base_request_data.token == TOKEN
    assert base_request_data.headers == {
        **BASE_API_HEADERS,
        HEADER_GITHUB_API_VERSION: "3000-01-01",
        "Authorization": "token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    }


@pytest.mark.asyncio
async def test_client_constrution_with_kwargs_timeout(client_session: ClientSession):
    client = GitHubClient(session=client_session, **{GitHubClientKwarg.TIMEOUT: 10})
    base_request_data = client._base_request_data
    assert base_request_data.timeout == 10


@pytest.mark.asyncio
async def test_client_constrution_with_kwargs_base_url(client_session: ClientSession):
    client = GitHubClient(
        session=client_session, **{GitHubClientKwarg.BASE_URL: "https://example.com"}
    )
    base_request_data = client._base_request_data
    assert base_request_data.base_url == "https://example.com"


@pytest.mark.asyncio
async def test_client_constrution_with_kwargs_headers(client_session: ClientSession):
    client = GitHubClient(
        session=client_session, **{GitHubClientKwarg.HEADERS: {"User-Agent": "test/client"}}
    )
    base_request_data = client._base_request_data
    assert base_request_data.headers["User-Agent"] == "test/client"


@pytest.mark.asyncio
async def test_client_constrution_with_kwargs_client_name(client_session: ClientSession):
    client = GitHubClient(
        session=client_session, **{GitHubClientKwarg.CLIENT_NAME: "test_client/1.2.3"}
    )
    base_request_data = client._base_request_data
    assert base_request_data.headers["User-Agent"] == "test_client/1.2.3"
