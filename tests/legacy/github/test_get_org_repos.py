# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json

import pytest

from aiogithubapi import GitHub
from aiogithubapi.common.exceptions import (
    AIOGitHubAPINotModifiedException,
    AIOGitHubAPIRatelimitException,
)
from tests.common import TOKEN
from tests.legacy.responses.base import base_response
from tests.legacy.responses.org_repositories import org_repositories_response


@pytest.mark.asyncio
async def test_get_org_repos(mock_response, org_repositories_response, client_session):
    mock_response.mock_data = org_repositories_response

    async with GitHub(TOKEN, session=client_session) as github:
        org = await github.get_org_repos("octocat")
        first_repo = org[0]
        assert first_repo.description == "This your first repo!"
        assert github.client.ratelimits.remaining == "4999"

        mock_response.clear()
        mock_response.mock_status = 304

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await github.get_org_repos("octocat", etag=github.client.last_response.etag)


@pytest.mark.asyncio
async def test_get_org_repos_ratelimited(github, mock_response):
    mock_response.mock_status = 403

    with pytest.raises(AIOGitHubAPIRatelimitException):
        await github.get_org_repos("octocat")
