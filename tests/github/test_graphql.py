"""Test graphql."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI, GitHubGraphQLException

from tests.common import MockedRequests, MockResponse


@pytest.mark.asyncio
async def test_graphql(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.graphql("test")
    assert response.status == 200
    assert isinstance(response.data, dict)
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/graphql"


@pytest.mark.asyncio
async def test_graphql_error(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = {"errors": [{"message": "test"}]}
    with pytest.raises(GitHubGraphQLException, match="test"):
        await github_api.graphql("test")

    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/graphql"
