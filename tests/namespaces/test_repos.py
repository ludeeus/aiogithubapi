"""Test repos namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI, GitHubRepositoryModel

from tests.common import TEST_REPOSITORY_NAME, MockedRequests


@pytest.mark.asyncio
async def test_get_repository(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.get(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, GitHubRepositoryModel)
    assert response.data.name == "Hello-World"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/repos/octocat/hello-world"


@pytest.mark.asyncio
async def test_list_commits(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.list_commits(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert response.data[0].commit.message == "Merge pull request #6"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/commits"
    )


@pytest.mark.asyncio
async def test_list_tags(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.list_tags(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert response.data[0].name == "v0.1"
    assert response.data[0].commit.sha == "c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"] == "https://api.github.com/repos/octocat/hello-world/tags"
    )
