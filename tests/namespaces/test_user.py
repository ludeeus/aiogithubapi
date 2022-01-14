"""Test users namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI

from tests.common import TEST_USER_NAME, MockedRequests


@pytest.mark.asyncio
async def test_get_authenticated_user(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.user.get()
    assert response.status == 200
    assert response.data.name == "The Octocat"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/user"


@pytest.mark.asyncio
async def test_get_authenticated_user_starred(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.user.starred()
    assert response.status == 200
    first_repo = response.data[0]
    assert first_repo.name == "Hello-World"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/user/starred"
