"""Test traffic namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI
from tests.common import TEST_REPOSITORY_NAME, MockedRequests


@pytest.mark.asyncio
async def test_clones(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.traffic.clones(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert len(response.data.clones) == 1
    assert response.data.clones[0].count == 1
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/traffic/clones"
    )


@pytest.mark.asyncio
async def test_views(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.traffic.views(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert len(response.data.views) == 1
    assert response.data.views[0].count == 1
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/traffic/views"
    )
