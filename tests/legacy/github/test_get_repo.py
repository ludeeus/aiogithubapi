# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json

import pytest

from aiogithubapi import (
    AIOGitHubAPINotModifiedException,
    AIOGitHubAPIRatelimitException,
    GitHub,
    GitHubAPI,
    GitHubNotModifiedException,
)
from aiogithubapi.const import GitHubRequestKwarg

from tests.common import EXPECTED_ETAG, TOKEN
from tests.legacy.responses.base import base_response
from tests.legacy.responses.repository_fixture import repository_response


@pytest.mark.asyncio
async def test_get_repo(mock_response, repository_response, client_session):
    mock_response.mock_data = repository_response

    async with GitHub(TOKEN, session=client_session) as github:
        repository = await github.get_repo("octocat/Hello-World")
        assert repository.description == "This your first repo!"
        assert github.client.last_response.etag == EXPECTED_ETAG
        assert github.client.ratelimits.remaining == "4999"

        mock_response.clear()
        mock_response.mock_status = 304

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await github.get_repo("octocat/Hello-World", github.client.last_response.etag)


@pytest.mark.asyncio
async def test_get_repo_ratelimited(mock_response, github):
    mock_response.mock_status = 403

    with pytest.raises(AIOGitHubAPIRatelimitException):
        await github.get_repo("octocat/Hello-World")
