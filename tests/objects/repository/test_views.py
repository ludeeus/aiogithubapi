# pylint: disable=missing-docstring, redefined-outer-name, unused-import

import json
import pytest
from aiogithubapi import GitHub
from aiogithubapi.objects.repository.views import AIOGitHubAPIRepositoryViews

from tests.const import TOKEN, NOT_RATELIMITED
from tests.responses.views_fixture import views_response


@pytest.mark.asyncio
async def test_views(aresponses, views_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/traffic/views",
        "get",
        aresponses.Response(
            text=json.dumps(views_response), status=200, headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        views = AIOGitHubAPIRepositoryViews()
        await views.get("octocat/Hello-World")
        assert views.count == 14850
        assert views.uniques == 3782
