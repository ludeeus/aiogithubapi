"""Test projects namespace."""
# pylint: disable=missing-docstring

from types import NoneType

import pytest

from aiogithubapi import GitHubAPI, GitHubProjectModel

from tests.common import (
    TEST_ORGANIZATION,
    TEST_REPOSITORY_NAME,
    MockedRequests,
    MockResponse,
    load_fixture,
)


@pytest.mark.asyncio
async def test_list_organization_projects(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.orgs.projects.list(TEST_ORGANIZATION)
    assert response.status == 200
    assert isinstance(response.data, list)
    fist = response.data[0]
    assert isinstance(fist, GitHubProjectModel)
    assert fist.name == "Organization Roadmap"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/orgs/octocat/projects"


@pytest.mark.asyncio
async def test_create_organization_project(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "orgs_octocat_projects.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.orgs.projects.create(TEST_ORGANIZATION, name="test", body="test")
    assert response.status == 200
    assert isinstance(response.data, GitHubProjectModel)
    assert response.data.name == "Organization Roadmap"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/orgs/octocat/projects"


@pytest.mark.asyncio
async def test_list_repository_projects(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.repos.projects.list(TEST_REPOSITORY_NAME)
    assert response.status == 200
    assert isinstance(response.data, list)
    fist = response.data[0]
    assert isinstance(fist, GitHubProjectModel)
    assert fist.name == "Projects Documentation"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/projects"
    )


@pytest.mark.asyncio
async def test_create_repository_project(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "repos_octocat_hello-world_projects.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.repos.projects.create(
        TEST_REPOSITORY_NAME, name="test", body="test"
    )
    assert response.status == 200
    assert isinstance(response.data, GitHubProjectModel)
    assert response.data.name == "Projects Documentation"
    assert mock_requests.called == 1
    assert (
        mock_requests.last_request["url"]
        == "https://api.github.com/repos/octocat/hello-world/projects"
    )


@pytest.mark.asyncio
async def test_list_users_projects(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.users.projects.list(TEST_ORGANIZATION)
    assert response.status == 200
    assert isinstance(response.data, list)
    fist = response.data[0]
    assert isinstance(fist, GitHubProjectModel)
    assert fist.name == "My Projects"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/users/octocat/projects"


@pytest.mark.asyncio
async def test_create_user_project(
    github_api: GitHubAPI,
    mock_requests: MockedRequests,
    mock_response: MockResponse,
):
    mock_response.mock_data = load_fixture(
        "users_octocat_projects.json",
        asjson=True,
        legacy=False,
    )[0]
    response = await github_api.user.projects.create(name="test", body="test")
    assert response.status == 200
    assert isinstance(response.data, GitHubProjectModel)
    assert response.data.name == "My Projects"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/user/projects"


@pytest.mark.asyncio
async def test_base_get_project(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.projects.get(project_id=1)
    assert response.status == 200
    assert isinstance(response.data, GitHubProjectModel)
    assert response.data.name == "Projects Documentation"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/projects/1"


@pytest.mark.asyncio
async def test_base_update_project(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.projects.update(project_id=1, data={"test": "update"})
    assert response.status == 200
    assert isinstance(response.data, GitHubProjectModel)
    assert response.data.name == "Projects Documentation"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/projects/1"


@pytest.mark.asyncio
async def test_base_delete_project(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.projects.delete(project_id=1)
    assert response.status == 200
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/projects/1"
