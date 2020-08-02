# pylint: disable=missing-docstring, redefined-outer-name, unused-import

import json
import pytest
from aiogithubapi import GitHub
from aiogithubapi.objects.repository.clones import AIOGitHubAPIRepositoryClones

from tests.const import TOKEN, NOT_RATELIMITED
from tests.responses.clones_fixture import clones_response


@pytest.mark.asyncio
async def test_clones(aresponses, clones_response, issue_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/traffic/clones",
        "get",
        aresponses.Response(
            text=json.dumps(clones_response), status=200, headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        clones = AIOGitHubAPIRepositoryClones()
        await clones.get("octocat/Hello-World")
        assert clones.count == 173
        assert clones.uniques == 128
