# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import datetime
import json

import pytest

from aiogithubapi import GitHub
from tests.const import NOT_RATELIMITED, TOKEN
from tests.responses.releases import releases_response
from tests.responses.repository_fixture import repository_response


@pytest.mark.asyncio
async def test_get_releases(aresponses, repository_response, releases_response):
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
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/releases",
        "get",
        aresponses.Response(
            text=json.dumps(releases_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/releases",
        "get",
        aresponses.Response(
            text=json.dumps(releases_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/releases",
        "get",
        aresponses.Response(
            text=json.dumps(releases_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        releases = await repository.get_releases()
        first = releases[0]
        assert first.tag_name == "v1.0.0"
        assert first.name == "v1.0.0"
        assert first.published_at == datetime.datetime(2013, 2, 27, 19, 35, 32)
        assert not first.draft
        assert not first.prerelease
        assert len(first.assets) == 1
