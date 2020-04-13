# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json
import aiohttp
import pytest
from aiogithubapi import AIOGitHub, AIOGitHubException

from tests.commmon import TOKEN
from tests.responses.headers import NOT_RATELIMITED, RATELIMITED
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
    async with aiohttp.ClientSession(loop=event_loop) as session:
        github = AIOGitHub(TOKEN, session)
        await github.get_ratelimit()
        assert github.client.ratelimits.remaining == "1337"


@pytest.mark.asyncio
async def test_get_ratelimit_error(aresponses, event_loop, base_response):
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(
            text=json.dumps(base_response), status=500, headers=NOT_RATELIMITED,
        ),
    )
    async with aiohttp.ClientSession(loop=event_loop) as session:
        github = AIOGitHub(TOKEN, session)
        with pytest.raises(AIOGitHubException):
            await github.get_ratelimit()
