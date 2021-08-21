# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json

import pytest

from aiogithubapi import (
    AIOGitHubAPIAuthenticationException,
    AIOGitHubAPIException,
    AIOGitHubAPIRatelimitException,
    GitHub,
)
from aiogithubapi.const import DEFAULT_USER_AGENT
from tests.common import HEADERS, HEADERS_RATELIMITED, TOKEN
from tests.legacy.responses.base import bad_auth_response, bad_response, base_response


@pytest.mark.asyncio
async def test_get(mock_response, client_session):

    async with GitHub(TOKEN, session=client_session) as github:
        await github.client.get("/")
        assert github.client.ratelimits.remaining == "4999"


@pytest.mark.asyncio
async def test_headers(mock_response, client_session):
    mock_response.mock_headers = HEADERS

    async with GitHub(TOKEN, session=client_session) as github:
        await github.client.get("/")
        assert github.client.headers["User-Agent"] == DEFAULT_USER_AGENT

    async with GitHub(
        TOKEN, headers={"User-Agent": "test/client"}, session=client_session
    ) as github:
        await github.client.get("/")
        assert github.client.headers["User-Agent"] == "test/client"


@pytest.mark.asyncio
async def test_post(mock_response, client_session):
    mock_response.mock_headers = HEADERS

    async with GitHub(session=client_session) as github:
        await github.client.post("/")
        assert github.client.ratelimits.remaining == "4999"


@pytest.mark.asyncio
async def test_post_with_json(mock_response, base_response, client_session):
    mock_response.mock_headers = HEADERS
    mock_response.mock_data = base_response

    async with GitHub(TOKEN, session=client_session) as github:
        await github.client.post("/", data={"test": "test"}, jsondata=True)
        assert github.client.ratelimits.remaining == "4999"


@pytest.mark.asyncio
async def test_get_ratelimited(client, mock_response):
    mock_response.mock_status = 403

    with pytest.raises(AIOGitHubAPIRatelimitException):
        await client.get("/")


@pytest.mark.asyncio
async def test_get_unauthorized(client, mock_response):
    mock_response.mock_status = 401

    with pytest.raises(AIOGitHubAPIAuthenticationException):
        await client.get("/")


@pytest.mark.asyncio
async def test_post_ratelimited(client, mock_response, base_response):
    mock_response.data = json.dumps(base_response)
    mock_response.mock_status = 403
    mock_response.mock_headers = HEADERS_RATELIMITED

    with pytest.raises(AIOGitHubAPIRatelimitException):
        await client.post("/")


@pytest.mark.asyncio
async def test_get_error(mock_response, client_session):
    mock_response.mock_status = 500

    async with GitHub(TOKEN, session=client_session) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.get("/")


@pytest.mark.asyncio
async def test_post_error(mock_response, client_session):
    mock_response.mock_status = 500

    async with GitHub(TOKEN, session=client_session) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.post("/")


@pytest.mark.asyncio
async def test_ok_get_auth_error(mock_response, bad_auth_response, client_session):
    mock_response.mock_data = bad_auth_response

    async with GitHub(TOKEN, session=client_session) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.get("/")


@pytest.mark.asyncio
async def test_ok_get_error(mock_response, bad_response, client_session):
    mock_response.mock_data = bad_response

    async with GitHub(TOKEN, session=client_session) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.get("/")


@pytest.mark.asyncio
async def test_custom_base_url(mock_response, mock_requests, client_session):
    mock_response.mock_headers = HEADERS

    async with GitHub(
        TOKEN, base_url="http://example.com", session=client_session
    ) as github:
        await github.client.get("/")
        assert github.client.ratelimits.remaining == "4999"

    assert mock_requests.last_request["url"] == "http://example.com/"
