"""Test orgs namespace."""
# pylint: disable=missing-docstring

import pytest

from aiogithubapi import (
    GitHubAPI,
    GitHubOrganizationMinimalModel,
    GitHubOrganizationModel,
)

from tests.common import TEST_ORGANIZATION, MockedRequests


@pytest.mark.asyncio
async def test_list_organizations(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.orgs.list()
    assert response.status == 200
    assert isinstance(response.data, list)
    fist = response.data[0]
    assert isinstance(fist, GitHubOrganizationMinimalModel)
    assert fist.login == "github"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/organizations"


@pytest.mark.asyncio
async def test_get_organization(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.orgs.get(TEST_ORGANIZATION)
    assert response.status == 200
    assert isinstance(response.data, GitHubOrganizationModel)
    assert response.data.name == "github"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/orgs/octocat"


@pytest.mark.asyncio
async def test_update_organization(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.orgs.update(TEST_ORGANIZATION, {"test": "data"})
    assert response.status == 200
    assert isinstance(response.data, GitHubOrganizationModel)
    assert response.data.name == "github"
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/orgs/octocat"
