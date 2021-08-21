"""Test rate_limit."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI
from tests.common import MockedRequests


@pytest.mark.asyncio
async def test_rate_limit(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.rate_limit()
    assert response.status == 200
    assert response.data.resources.core.limit == 5000
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/rate_limit"
