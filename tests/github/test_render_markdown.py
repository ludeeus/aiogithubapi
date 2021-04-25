# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aiogithubapi import AIOGitHubAPIException, AIOGitHubAPINotModifiedException, GitHub
from aiogithubapi.common.exceptions import AIOGitHubAPIRatelimitException
from tests.const import NOT_RATELIMITED, RATELIMITED, TOKEN
from tests.responses.base import base_response


@pytest.mark.asyncio
async def test_render_markdown(aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/markdown/raw",
        "post",
        aresponses.Response(
            text=json.dumps(base_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/markdown/raw",
        "post",
        aresponses.Response(status=304),
    )
    async with GitHub(TOKEN) as github:
        render = await github.render_markdown("test")
        assert github.client.ratelimits.remaining == "1337"
        assert isinstance(render, str)

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await github.render_markdown("test", etag=github.client.last_response.etag)


@pytest.mark.asyncio
async def test_render_markdown_rate_limited(aresponses, github, base_response):
    aresponses.add(
        "api.github.com",
        "/markdown/raw",
        "post",
        aresponses.Response(
            text=json.dumps(base_response),
            status=403,
            headers=RATELIMITED,
        ),
    )
    with pytest.raises(AIOGitHubAPIRatelimitException):
        await github.render_markdown("test")


@pytest.mark.asyncio
async def test_render_markdown_error(aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/markdown/raw",
        "post",
        aresponses.Response(
            text=json.dumps(base_response),
            status=500,
            headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.render_markdown("test")
