"""Test repos namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI, GitHubRepositoryModel
from aiogithubapi.const import HttpContentType

from tests.common import (
    HEADERS,
    HEADERS_TEXT,
    TEST_REPOSITORY_NAME,
    MockedRequests,
    MockResponse,
)


@pytest.mark.asyncio
async def test_get_repository(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.get(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, GitHubRepositoryModel)
    assert response.data.name == "Hello-World"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/repos/octocat/hello-world"


@pytest.mark.asyncio
async def test_list_commits(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.list_commits(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert response.data[0].commit.message == "Merge pull request #6"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/commits"
    )


@pytest.mark.asyncio
async def test_list_tags(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.list_tags(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert response.data[0].name == "v0.1"
    assert response.data[0].commit.sha == "c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"] == "https://api.github.com/repos/octocat/hello-world/tags"
    )


@pytest.mark.asyncio
async def test_tarball(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_headers = {**HEADERS, "content-type": HttpContentType.BASE_GZIP}
    response = await github_api.repos.tarball("octocat/hello-world")
    assert isinstance(response.data, bytes)
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/tarball/"
    )
    response = await github_api.repos.tarball("octocat/hello-world", ref="main")
    assert isinstance(response.data, bytes)
    assert mock_requests.called == 2
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/tarball/main"
    )


@pytest.mark.asyncio
async def test_zipball(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_headers = {**HEADERS, "content-type": HttpContentType.BASE_ZIP}
    response = await github_api.repos.zipball("octocat/hello-world")
    assert isinstance(response.data, bytes)
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/zipball/"
    )
    response = await github_api.repos.zipball("octocat/hello-world", ref="main")
    assert isinstance(response.data, bytes)
    assert mock_requests.called == 2
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/zipball/main"
    )


@pytest.mark.asyncio
async def test_readme(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_headers = HEADERS_TEXT

    response = await github_api.repos.readme(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, str)
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/readme/"
    )

    response = await github_api.repos.readme(TEST_REPOSITORY_NAME, dir="test")
    assert response.status == 200
    assert isinstance(response.data, str)
    assert mock_requests.called == 2
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/readme/test"
    )
