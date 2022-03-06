"""Test octocat."""
# pylint: disable=missing-docstring
from aiohttp.hdrs import CONTENT_TYPE
import pytest

from aiogithubapi import GitHubAPI
from aiogithubapi.const import HttpContentType

from tests.common import HEADERS, MockedRequests, MockResponse


@pytest.mark.asyncio
async def test_octocat(
    github_api: GitHubAPI,
    mock_response: MockResponse,
    mock_requests: MockedRequests,
):
    mock_response.mock_headers = {**HEADERS, CONTENT_TYPE: HttpContentType.TEXT_PLAIN}
    response = await github_api.octocat()
    assert response.status == 200
    assert "Encourage flow." in response.data
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/octocat"
