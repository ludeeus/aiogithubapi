"""Test releases namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI, GitHubReleaseModel

from tests.common import TEST_REPOSITORY_NAME, MockedRequests


@pytest.mark.asyncio
async def test_list_releases(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.releases.list(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert isinstance(response.data[0], GitHubReleaseModel)
    assert response.data[0].name == "First release"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/releases"
    )

@pytest.mark.asyncio
async def test_latest(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.releases.latest(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, GitHubReleaseModel)
    assert response.data.name == "First release"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/releases/latest"
    )

def test_release_without_author():
    """A release whose author account no longer exists has author null."""
    release = GitHubReleaseModel({"name": "First release", "author": None})
    assert release.name == "First release"
    assert release.author is None
