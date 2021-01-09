# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aiogithubapi import AIOGitHubAPIException, GitHub
from aiogithubapi.common.exceptions import AIOGitHubAPIRatelimitException
from tests.const import NOT_RATELIMITED, RATELIMITED, TOKEN
from tests.responses.base import base_response
from tests.responses.repository_fixture import repository_response


@pytest.mark.asyncio
async def test_get_repo(aresponses, event_loop, repository_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        assert repository.description == "This your first repo!"
        assert github.client.ratelimits.remaining == "1337"


@pytest.mark.asyncio
async def test_get_repo_ratelimited(aresponses, github, base_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(base_response),
            status=403,
            headers=RATELIMITED,
        ),
    )
    with pytest.raises(AIOGitHubAPIRatelimitException):
        await github.get_repo("octocat/Hello-World")
