"""Test releases namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI

from tests.common import TEST_REPOSITORY_NAME, MockedRequests


@pytest.mark.asyncio
async def test_list_releases(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.releases.list(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert response.data[0].name == "First release"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/releases"
    )
