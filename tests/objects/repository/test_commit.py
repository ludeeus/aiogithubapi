# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import datetime
import json
import pytest
from aiogithubapi import GitHub

from tests.const import TOKEN, NOT_RATELIMITED
from tests.responses.repository_fixture import repository_response
from tests.responses.repos.branch_fixtrue import branch_fixtrue_response


@pytest.mark.asyncio
async def test_get_last_commit(
    aresponses, repository_response, branch_fixtrue_response
):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/branches/master",
        "get",
        aresponses.Response(
            text=json.dumps(branch_fixtrue_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        commit = await repository.get_last_commit()
        assert commit.sha == "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d"
