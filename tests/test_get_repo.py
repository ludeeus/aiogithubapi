# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json
import aiohttp
import pytest
from aiogithubapi import AIOGitHub, AIOGitHubException

from tests.commmon import TOKEN
from tests.responses.headers import NOT_RATELIMITED, RATELIMITED
from tests.responses.base import base_response
from tests.responses.repository import repository_response


@pytest.mark.asyncio
async def test_get_repo(aresponses, event_loop, repository_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    async with aiohttp.ClientSession(loop=event_loop) as session:
        github = AIOGitHub(TOKEN, session)
        repository = await github.get_repo("octocat/Hello-World")
        assert repository.description == "This your first repo!"


@pytest.mark.asyncio
async def test_get_repo_ratelimited(aresponses, event_loop, base_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(base_response), status=403, headers=RATELIMITED,
        ),
    )
    async with aiohttp.ClientSession(loop=event_loop) as session:
        github = AIOGitHub(TOKEN, session)
        with pytest.raises(AIOGitHubException):
            await github.get_repo("octocat/Hello-World")
