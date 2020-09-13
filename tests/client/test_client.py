# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json
import aiohttp
import pytest
from aiogithubapi import GitHub, AIOGitHubAPIException

from tests.const import TOKEN, NOT_RATELIMITED, RATELIMITED
from tests.responses.base import bad_response, base_response, bad_auth_response


@pytest.mark.asyncio
async def test_get(aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/",
        "get",
        aresponses.Response(
            text=json.dumps(base_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        await github.client.get("/")
        assert github.client.ratelimits.remaining == "1337"


@pytest.mark.asyncio
async def test_post(aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/",
        "post",
        aresponses.Response(
            text=json.dumps(base_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub() as github:
        await github.client.post("/")
        assert github.client.ratelimits.remaining == "1337"


@pytest.mark.asyncio
async def test_post_with_json(aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/",
        "post",
        aresponses.Response(
            text=json.dumps(base_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        await github.client.post("/", data={"test": "test"}, jsondata=True)
        assert github.client.ratelimits.remaining == "1337"


@pytest.mark.asyncio
async def test_get_ratelimited(aresponses, bad_auth_response):
    aresponses.add(
        "api.github.com",
        "/",
        "get",
        aresponses.Response(
            text=json.dumps(bad_auth_response),
            status=403,
            headers=RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.get("/")
        assert github.client.ratelimits.remaining == "0"


@pytest.mark.asyncio
async def test_post_ratelimited(aresponses, bad_auth_response):
    aresponses.add(
        "api.github.com",
        "/",
        "post",
        aresponses.Response(
            text=json.dumps(bad_auth_response),
            status=403,
            headers=RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.post("/")
        assert github.client.ratelimits.remaining == "0"


@pytest.mark.asyncio
async def test_get_error(aresponses, bad_response):
    aresponses.add(
        "api.github.com",
        "/",
        "get",
        aresponses.Response(
            text=json.dumps(bad_response),
            status=500,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.get("/")


@pytest.mark.asyncio
async def test_post_error(aresponses, bad_response):
    aresponses.add(
        "api.github.com",
        "/",
        "post",
        aresponses.Response(
            text=json.dumps(bad_response),
            status=500,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.post("/")


@pytest.mark.asyncio
async def test_ok_get_auth_error(aresponses, bad_auth_response):
    aresponses.add(
        "api.github.com",
        "/",
        "get",
        aresponses.Response(
            text=json.dumps(bad_auth_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.get("/")


@pytest.mark.asyncio
async def test_ok_get_error(aresponses, bad_response):
    aresponses.add(
        "api.github.com",
        "/",
        "get",
        aresponses.Response(
            text=json.dumps(bad_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        with pytest.raises(AIOGitHubAPIException):
            await github.client.get("/")
