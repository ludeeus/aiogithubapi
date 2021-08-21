"""Test generic api call."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI
from tests.common import (
    HEADERS_TEXT,
    TEST_REPOSITORY_NAME,
    MockedRequests,
    MockResponse,
)


@pytest.mark.asyncio
async def test_markdown_base(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_headers = HEADERS_TEXT
    response = await github_api.markdown("Lorem ipsum...")
    assert response.status == 200
    assert response.data == "Lorem ipsum..."
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "post"
    assert mock_requests.last_request["url"] == "https://api.github.com/markdown"
    assert mock_requests.last_request["json"] == {
        "context": None,
        "mode": None,
        "text": "Lorem ipsum...",
    }


@pytest.mark.asyncio
async def test_markdown_mode(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_headers = HEADERS_TEXT
    response = await github_api.markdown("Lorem ipsum...", mode="gfm")
    assert response.status == 200
    assert response.data == "Lorem ipsum..."
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "post"
    assert mock_requests.last_request["url"] == "https://api.github.com/markdown"
    assert mock_requests.last_request["json"] == {
        "context": None,
        "mode": "gfm",
        "text": "Lorem ipsum...",
    }


@pytest.mark.asyncio
async def test_markdown_context(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_headers = HEADERS_TEXT
    response = await github_api.markdown("Lorem ipsum...", context=TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert response.data == "Lorem ipsum..."
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "post"
    assert mock_requests.last_request["url"] == "https://api.github.com/markdown"
    assert mock_requests.last_request["json"] == {
        "context": TEST_REPOSITORY_NAME,
        "mode": "gfm",
        "text": "Lorem ipsum...",
    }
