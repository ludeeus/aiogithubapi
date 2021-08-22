"""Test generic api call."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI, GitHubRequestKwarg

from tests.common import MockedRequests


@pytest.mark.asyncio
async def test_generic_get(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.generic("/generic")
    assert response.status == 200
    assert response.data == {}
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "get"
    assert mock_requests.last_request["url"] == "https://api.github.com/generic"


@pytest.mark.asyncio
async def test_generic_post(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.generic("/generic", **{GitHubRequestKwarg.METHOD: "POST"})
    assert response.status == 200
    assert response.data == {}
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "post"
    assert mock_requests.last_request["url"] == "https://api.github.com/generic"
    assert mock_requests.last_request["data"] is None
    assert "json" not in mock_requests.last_request


@pytest.mark.asyncio
async def test_generic_post_with_data(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.generic(
        "/generic", {"test": "data"}, **{GitHubRequestKwarg.METHOD: "POST"}
    )
    assert response.status == 200
    assert response.data == {}
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "post"
    assert mock_requests.last_request["url"] == "https://api.github.com/generic"
    assert mock_requests.last_request["json"] == {"test": "data"}
