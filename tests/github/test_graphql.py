"""Test graphql."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI
from tests.common import MockedRequests


@pytest.mark.asyncio
async def test_graphql(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.graphql("test")
    assert response.status == 200
    assert isinstance(response.data, dict)
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/graphql"
