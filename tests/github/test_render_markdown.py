# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json
import aiohttp
import pytest
from aiogithubapi import GitHub, AIOGitHubAPIException

from tests.const import TOKEN, NOT_RATELIMITED, RATELIMITED
from tests.responses.base import base_response


@pytest.mark.asyncio
async def test_render_markdown(aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/markdown/raw",
        "post",
        aresponses.Response(
            text=json.dumps(base_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        render = await github.render_markdown("test")
        assert github.client.ratelimits.remaining == "1337"
        assert isinstance(render, str)


@pytest.mark.asyncio
async def test_render_markdown_rate_limited(aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/markdown/raw",
        "post",
        aresponses.Response(
            text=json.dumps(base_response), status=403, headers=RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.render_markdown("test")
        assert github.client.ratelimits.remaining == "0"


@pytest.mark.asyncio
async def test_render_markdown_error(aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/markdown/raw",
        "post",
        aresponses.Response(
            text=json.dumps(base_response), status=500, headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.render_markdown("test")
