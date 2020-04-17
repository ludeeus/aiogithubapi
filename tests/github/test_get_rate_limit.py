# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json
import aiohttp
import pytest
from aiogithubapi import GitHub, AIOGitHubAPIException

from tests.const import TOKEN, NOT_RATELIMITED, RATELIMITED
from tests.responses.base import base_response


@pytest.mark.asyncio
async def test_get_rate_limit(aresponses, event_loop, base_response):
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(
            text=json.dumps(base_response), status=200, headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        rate_limit = await github.get_rate_limit()
        assert rate_limit["remaining"] == "1337"
