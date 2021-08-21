# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aiogithubapi import AIOGitHubAPIException, AIOGitHubAPINotModifiedException, GitHub
from aiogithubapi.common.exceptions import AIOGitHubAPIRatelimitException
from tests.common import TOKEN
from tests.legacy.responses.base import base_response


@pytest.mark.asyncio
async def test_render_markdown(mock_response, base_response, client_session):
    mock_response.mock_data = json.dumps(base_response)

    async with GitHub(TOKEN, session=client_session) as github:
        render = await github.render_markdown("test")
        assert github.client.ratelimits.remaining == "4999"
        assert isinstance(render, str)

        mock_response.clear()
        mock_response.mock_status = 304

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await github.render_markdown("test", etag=github.client.last_response.etag)


@pytest.mark.asyncio
async def test_render_markdown_rate_limited(mock_response, github):
    mock_response.mock_status = 403
    with pytest.raises(AIOGitHubAPIRatelimitException):
        await github.render_markdown("test")


@pytest.mark.asyncio
async def test_render_markdown_error(mock_response, client_session):
    mock_response.mock_status = 500

    async with GitHub(TOKEN, session=client_session) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.render_markdown("test")
