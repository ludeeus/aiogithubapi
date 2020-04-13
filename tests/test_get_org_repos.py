# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json
import aiohttp
import pytest
from aiogithubapi import AIOGitHub, AIOGitHubException

from tests.commmon import TOKEN
from tests.responses.headers import NOT_RATELIMITED, RATELIMITED
from tests.responses.base import base_response
from tests.responses.org_repositories import org_repositories_response


@pytest.mark.asyncio
async def test_get_org_repos(aresponses, event_loop, org_repositories_response):
    aresponses.add(
        "api.github.com",
        "/orgs/octocat/repos",
        "get",
        aresponses.Response(
            text=json.dumps(org_repositories_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    async with aiohttp.ClientSession(loop=event_loop) as session:
        github = AIOGitHub(TOKEN, session)
        org = await github.get_org_repos("octocat")
        first_repo = org[0]
        assert first_repo.description == "This your first repo!"
        assert github.client.ratelimits.remaining == "1337"


@pytest.mark.asyncio
async def test_get_org_repos_ratelimited(aresponses, event_loop, base_response):
    aresponses.add(
        "api.github.com",
        "/orgs/octocat/repos",
        "get",
        aresponses.Response(
            text=json.dumps(base_response), status=403, headers=RATELIMITED,
        ),
    )
    async with aiohttp.ClientSession(loop=event_loop) as session:
        github = AIOGitHub(TOKEN, session)
        with pytest.raises(AIOGitHubException):
            await github.get_org_repos("octocat")
        assert github.client.ratelimits.remaining == "0"
