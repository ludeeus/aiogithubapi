# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json

import pytest

from aiogithubapi import GitHub
from aiogithubapi.common.exceptions import (
    AIOGitHubAPIRatelimitException,
    AIOGitHubAPINotModifiedException,
)
from tests.const import NOT_RATELIMITED, RATELIMITED, TOKEN
from tests.responses.base import base_response
from tests.responses.org_repositories import org_repositories_response


@pytest.mark.asyncio
async def test_get_org_repos(aresponses, org_repositories_response):
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
    aresponses.add(
        "api.github.com",
        "/orgs/octocat/repos",
        "get",
        aresponses.Response(
            text="",
            status=304,
        ),
    )

    async with GitHub(TOKEN) as github:
        org = await github.get_org_repos("octocat")
        first_repo = org[0]
        assert first_repo.description == "This your first repo!"
        assert github.client.ratelimits.remaining == "1337"

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await github.get_org_repos("octocat", etag=github.client.last_response.etag)


@pytest.mark.asyncio
async def test_get_org_repos_ratelimited(github, aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/orgs/octocat/repos",
        "get",
        aresponses.Response(
            text=json.dumps(base_response),
            status=403,
            headers=RATELIMITED,
        ),
    )

    with pytest.raises(AIOGitHubAPIRatelimitException):
        await github.get_org_repos("octocat")
