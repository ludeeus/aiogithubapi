# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json
import datetime
import pytest
from aiogithubapi import GitHub, AIOGitHubAPIException

from tests.const import TOKEN, NOT_RATELIMITED, RATELIMITED
from tests.responses.base import base_response
from tests.responses.repository import repository_response
from tests.responses.branch import branch_response


@pytest.mark.asyncio
async def test_get_repository(aresponses, repository_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        assert repository.description == "This your first repo!"
        assert repository.id == 1296269
        assert repository.full_name == "octocat/Hello-World"
        assert repository.pushed_at == datetime.datetime(2011, 1, 26, 19, 6, 43)
        assert not repository.archived
        assert repository.topics == ["octocat", "atom", "electron", "api"]
        assert not repository.fork
        assert repository.default_branch == "master"
        assert repository.last_commit is None


@pytest.mark.asyncio
async def test_set_last_commit(aresponses, repository_response, branch_response):
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
        "/repos/octocat/Hello-World/commits/master",
        "get",
        aresponses.Response(
            text=json.dumps(branch_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        assert repository.last_commit is None
        await repository.set_last_commit()
