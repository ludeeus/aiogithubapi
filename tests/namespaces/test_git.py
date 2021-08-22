"""Test git namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI

from tests.common import TEST_REPOSITORY_NAME, MockedRequests


@pytest.mark.asyncio
async def test_get_tree(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.git.get_tree(TEST_REPOSITORY_NAME, "master")
    assert response.status == 200
    assert response.data.tree[0].path == "README"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/git/trees/master"
    )
