"""Test contents namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI, GitHubContentsModel

from tests.common import TEST_REPOSITORY_NAME, MockedRequests


@pytest.mark.asyncio
async def test_get_root(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.contents.get(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1
    assert response.data[0].name == "README"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/contents"
    )


@pytest.mark.asyncio
async def test_get_readme(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.contents.get(TEST_REPOSITORY_NAME, "README")
    assert response.status == 200
    assert isinstance(response.data, GitHubContentsModel)
    assert response.data.name == "README"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/contents/README"
    )
