"""Test zen."""
# pylint: disable=missing-docstring
from aiohttp.hdrs import CONTENT_TYPE
import pytest

from aiogithubapi import GitHubAPI
from aiogithubapi.const import HttpContentType

from tests.common import MockedRequests, MockResponse


@pytest.mark.asyncio
async def test_versions(
    github_api: GitHubAPI,
    mock_response: MockResponse,
    mock_requests: MockedRequests,
):
    response = await github_api.versions()
    assert response.status == 200
    assert response.data[0] == "2022-11-28"
    assert response.headers.x_github_api_version_selected == "2022-11-28"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/versions"
