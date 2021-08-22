"""Test contents namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI

from tests.common import TEST_REPOSITORY_NAME, MockedRequests, MockResponse


@pytest.mark.asyncio
async def test_list(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.pulls.list(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1
    assert response.data[0].title == "Awesome title"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/pulls"
    )


@pytest.mark.asyncio
async def test_list_empty(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = []
    response = await github_api.repos.pulls.list(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 0
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/pulls"
    )
