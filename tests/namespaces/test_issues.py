"""Test issues namespace."""
import pytest

from aiogithubapi import GitHubAPI, GitHubIssueCommentModel, GitHubIssueModel

from tests.common import (
    TEST_REPOSITORY_NAME,
    MockedRequests,
    MockResponse,
    load_fixture,
)


@pytest.mark.asyncio
async def test_list(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.issues.list(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1
    assert response.data[0].title == "Test issue"
    assert not response.data[0].is_pull_request
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues"
    )


@pytest.mark.asyncio
async def test_get(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "repos_octocat_hello-world_issues.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.repos.issues.get(TEST_REPOSITORY_NAME, 1)
    assert response.status == 200
    assert isinstance(response.data, GitHubIssueModel)
    assert response.data.title == "Test issue"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/1"
    )


@pytest.mark.asyncio
async def test_get_pull_request_from_issues_namespace(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = {
        **load_fixture(
            "repos_octocat_hello-world_issues.json",
            asjson=True,
            legacy=False,
        )[0],
        "pull_request": {"url": ""},
    }
    response = await github_api.repos.issues.get(TEST_REPOSITORY_NAME, 1)
    assert response.status == 200
    assert isinstance(response.data, GitHubIssueModel)
    assert response.data.title == "Test issue"
    assert isinstance(response.data.as_dict, dict)
    assert response.data.is_pull_request
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/1"
    )


@pytest.mark.asyncio
async def test_create(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "repos_octocat_hello-world_issues.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.repos.issues.create(TEST_REPOSITORY_NAME, {"title": "test"})
    assert response.status == 200
    assert isinstance(response.data, GitHubIssueModel)
    assert response.data.title == "Test issue"
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "post"
    assert mock_requests.last_request["json"] == {"title": "test"}
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues"
    )


@pytest.mark.asyncio
async def test_update(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "repos_octocat_hello-world_issues.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.repos.issues.update(TEST_REPOSITORY_NAME, 1, {"title": "test"})
    assert response.status == 200
    assert isinstance(response.data, GitHubIssueModel)
    assert response.data.title == "Test issue"
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "patch"
    assert mock_requests.last_request["json"] == {"title": "test"}
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/1"
    )


@pytest.mark.asyncio
async def test_lock(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_status = 204
    response = await github_api.repos.issues.lock(TEST_REPOSITORY_NAME, 1, "spam")
    assert response.status == 204
    assert response.data is None
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "put"
    assert mock_requests.last_request["json"] == {"lock_reason": "spam"}
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/1/lock"
    )


@pytest.mark.asyncio
async def test_unlock(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_status = 204
    response = await github_api.repos.issues.unlock(TEST_REPOSITORY_NAME, 1)
    assert response.status == 204
    assert response.data is None
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "delete"
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/1/lock"
    )


@pytest.mark.asyncio
async def test_list_comments(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.issues.list_comments(TEST_REPOSITORY_NAME, 1)
    assert response.status == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1
    assert response.data[0].body == "No logs, no issue!"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/1/comments"
    )


@pytest.mark.asyncio
async def test_get_comment(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "repos_octocat_hello-world_issues_1_comments.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.repos.issues.get_comment(TEST_REPOSITORY_NAME, 1)
    assert response.status == 200
    assert isinstance(response.data, GitHubIssueCommentModel)
    assert response.data.body == "No logs, no issue!"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/comments/1"
    )


@pytest.mark.asyncio
async def test_create_comment(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "repos_octocat_hello-world_issues_1_comments.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.repos.issues.create_comment(
        TEST_REPOSITORY_NAME, 1, {"title": "test"}
    )
    assert response.status == 200
    assert isinstance(response.data, GitHubIssueCommentModel)
    assert response.data.body == "No logs, no issue!"
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "post"
    assert mock_requests.last_request["json"] == {"title": "test"}
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/1/comments"
    )


@pytest.mark.asyncio
async def test_update_comment(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "repos_octocat_hello-world_issues_1_comments.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.repos.issues.update_comment(
        TEST_REPOSITORY_NAME, 1, {"title": "test"}
    )
    assert response.status == 200
    assert isinstance(response.data, GitHubIssueCommentModel)
    assert response.data.body == "No logs, no issue!"
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "patch"
    assert mock_requests.last_request["json"] == {"title": "test"}
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/comments/1"
    )


@pytest.mark.asyncio
async def test_delete_comment(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_status = 204
    response = await github_api.repos.issues.delete_comment(TEST_REPOSITORY_NAME, 1)
    assert response.status == 204
    assert response.data is None
    assert mock_requests.called == 1
    assert mock_requests.last_request["method"] == "delete"
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/issues/comments/1"
    )
