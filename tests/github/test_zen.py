"""Test zen."""
# pylint: disable=missing-docstring
import pytest
from aiohttp.hdrs import CONTENT_TYPE

from aiogithubapi import GitHubAPI
from aiogithubapi.const import HttpContentType
from tests.common import MockedRequests, MockResponse


@pytest.mark.asyncio
async def test_zen(
    github_api: GitHubAPI,
    mock_response: MockResponse,
    mock_requests: MockedRequests,
):
    mock_response.mock_headers = {CONTENT_TYPE: HttpContentType.TEXT_PLAIN}
    response = await github_api.zen()
    assert response.status == 200
    assert response.data == "Beautiful is better than ugly."
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/zen"
