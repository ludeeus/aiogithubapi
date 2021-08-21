"""Test client construction"""
# pylint: disable=missing-docstring,protected-access
import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from aiogithubapi import (
    GitHubAPI,
    GitHubAuthenticationException,
    GitHubConnectionException,
    GitHubException,
    GitHubRatelimitException,
)
from aiogithubapi.const import GitHubRequestKwarg
from tests.common import (
    EXPECTED_ETAG,
    TEST_REQUEST_HEADERS,
    MockedRequests,
    MockResponse,
)


@pytest.mark.asyncio
async def test_passing_etag_to_request(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
):
    response = await github_api.generic("/generic")
    assert response.status == 200
    assert "If-None-Match" not in mock_requests.last_request["headers"]
    mock_requests.clear()

    response = await github_api.generic("/generic", **{GitHubRequestKwarg.ETAG: "test"})
    assert response.status == 200
    assert mock_requests.last_request["headers"]["If-None-Match"] == "test"


@pytest.mark.asyncio
async def test_passing_headers_to_request(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
):
    response = await github_api.generic("/generic")
    assert response.status == 200
    assert mock_requests.last_request["headers"] == TEST_REQUEST_HEADERS
    mock_requests.clear()

    response = await github_api.generic(
        "/generic", **{GitHubRequestKwarg.HEADERS: {"test": "test"}}
    )
    assert response.status == 200
    assert mock_requests.last_request["headers"] == {
        **TEST_REQUEST_HEADERS,
        "test": "test",
    }


@pytest.mark.asyncio
async def test_passing_params_to_request(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
):
    response = await github_api.generic("/generic")
    assert response.status == 200
    assert mock_requests.last_request["params"] == {}
    mock_requests.clear()

    response = await github_api.generic(
        "/generic", **{GitHubRequestKwarg.PARAMS: {"test": "test"}}
    )
    assert response.status == 200
    assert mock_requests.last_request["params"] == {"test": "test"}
    mock_requests.clear()

    response = await github_api.generic(
        "/generic", **{GitHubRequestKwarg.QUERY: {"test": "test"}}
    )
    assert response.status == 200
    assert mock_requests.last_request["params"] == {"test": "test"}


@pytest.mark.asyncio
async def test_passing_method_to_request(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
):
    response = await github_api.generic("/generic")
    assert response.status == 200
    assert mock_requests.last_request["method"] == "get"
    mock_requests.clear()

    response = await github_api.generic(
        "/generic", **{GitHubRequestKwarg.METHOD: "POST"}
    )
    assert response.status == 200
    assert mock_requests.last_request["method"] == "post"


@pytest.mark.asyncio
async def test_client_exceptions(github_api: GitHubAPI):
    with patch(
        "aiohttp.ClientSession.request", side_effect=aiohttp.ClientError("client_error")
    ):
        with pytest.raises(
            GitHubConnectionException,
            match="Request exception for 'https://api.github.com/generic' with - client_error",
        ):
            await github_api.generic("/generic")

    with patch(
        "aiohttp.ClientSession.request",
        side_effect=asyncio.CancelledError("cancelation_error"),
    ):
        with pytest.raises(
            GitHubConnectionException,
            match="Request exception for 'https://api.github.com/generic' with - cancelation_error",
        ):
            await github_api.generic("/generic")

    with patch("aiohttp.ClientSession.request", side_effect=asyncio.TimeoutError):
        with pytest.raises(
            GitHubConnectionException,
            match="Timeout of 20 reached while waiting for https://api.github.com/generic",
        ):
            await github_api.generic("/generic")

    with patch(
        "aiohttp.ClientSession.request", side_effect=BaseException("Eeeeeh... okey?")
    ):
        with pytest.raises(
            GitHubException,
            match="Unexpected exception for "
            "'https://api.github.com/generic' with - Eeeeeh... okey?",
        ):
            await github_api.generic("/generic")


@pytest.mark.asyncio
async def test_status_code_handling(github_api: GitHubAPI, mock_response: MockResponse):
    mock_response.mock_data = {"message": "Not Found"}
    with pytest.raises(GitHubException, match="{'message': 'Not Found'}"):
        await github_api.generic("/generic")
    mock_response.clear()

    mock_response.mock_data = {"message": "Bad credentials"}
    with pytest.raises(
        GitHubAuthenticationException, match="Access token is not valid!"
    ):
        await github_api.generic("/generic")
    mock_response.clear()

    mock_response.mock_status = 403
    mock_response.mock_data = {"message": "rate limited"}
    with pytest.raises(GitHubRatelimitException, match="{'message': 'rate limited'}"):
        await github_api.generic("/generic")
    mock_response.clear()

    mock_response.mock_status = 403
    mock_response.mock_data = {"message": "Bad credentials"}
    with pytest.raises(
        GitHubAuthenticationException, match="{'message': 'Bad credentials'}"
    ):
        await github_api.generic("/generic")
    mock_response.clear()

    mock_response.mock_status = 204
    response = await github_api.generic("/generic")
    assert response.data is None


@pytest.mark.asyncio
async def test_response_object(github_api: GitHubAPI, mock_response: MockResponse):
    response = await github_api.generic("/generic")
    assert response.etag == EXPECTED_ETAG
    assert response.page_number == 2
    assert response.next_page_number == 3
    assert response.last_page_number == 46
    assert not response.is_last_page

    mock_response.mock_headers = {"Link": None}
    response = await github_api.generic("/generic")
    assert response.is_last_page
    assert response.page_number == 1
    assert response.next_page_number is None
    assert response.last_page_number is None
    assert response.pages == {}

    mock_response.mock_headers = {"Link": ""}
    response = await github_api.generic("/generic")
    assert response.page_number == 1
