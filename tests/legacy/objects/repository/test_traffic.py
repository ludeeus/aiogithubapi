# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import datetime
import json

import pytest

from aiogithubapi import AIOGitHubAPINotModifiedException, GitHub

from tests.common import TOKEN
from tests.legacy.responses.repos.traffic.clones_fixtrue import clones_fixtrue_response
from tests.legacy.responses.repos.traffic.pageviews_fixtrue import (
    pageviews_fixtrue_response,
)
from tests.legacy.responses.repository_fixture import repository_response


@pytest.mark.asyncio
async def test_get_clones(aresponses, repository_response, clones_fixtrue_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/traffic/clones",
        "get",
        aresponses.Response(
            text=json.dumps(clones_fixtrue_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/traffic/clones",
        "get",
        aresponses.Response(status=304),
    )

    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        clones = await repository.traffic.get_clones()
        assert clones.count == 173

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await repository.traffic.get_clones(etag=github.client.last_response.etag)


@pytest.mark.asyncio
async def test_get_views(aresponses, repository_response, pageviews_fixtrue_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/traffic/views",
        "get",
        aresponses.Response(
            text=json.dumps(pageviews_fixtrue_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/traffic/views",
        "get",
        aresponses.Response(status=304),
    )

    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        views = await repository.traffic.get_views()
        assert views.count == 14850

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await repository.traffic.get_views(etag=github.client.last_response.etag)
