# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import json

import pytest

from aiogithubapi import AIOGitHubAPIException, GitHub
from aiogithubapi.common.exceptions import (
    AIOGitHubAPIAuthenticationException,
    AIOGitHubAPIRatelimitException,
)
from tests.const import NOT_RATELIMITED, RATELIMITED, TOKEN
from tests.responses.base import bad_auth_response, bad_response, base_response


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
async def test_headers(aresponses, base_response):
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
        assert github.client.headers["User-Agent"] == "python/AIOGitHubAPI"

    async with GitHub(TOKEN, headers={"User-Agent": "test/client"}) as github:
        await github.client.get("/")
        assert github.client.headers["User-Agent"] == "test/client"


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
async def test_get_ratelimited(client, aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/",
        "get",
        aresponses.Response(
            text=json.dumps(base_response),
            status=403,
            headers=RATELIMITED,
        ),
    )

    with pytest.raises(AIOGitHubAPIRatelimitException):
        await client.get("/")


@pytest.mark.asyncio
async def test_get_unauthorized(client, aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/",
        "get",
        aresponses.Response(
            text=json.dumps(base_response),
            status=401,
            headers=NOT_RATELIMITED,
        ),
    )

    with pytest.raises(AIOGitHubAPIAuthenticationException):
        await client.get("/")


@pytest.mark.asyncio
async def test_post_ratelimited(client, aresponses, base_response):
    aresponses.add(
        "api.github.com",
        "/",
        "post",
        aresponses.Response(
            text=json.dumps(base_response),
            status=403,
            headers=RATELIMITED,
        ),
    )

    with pytest.raises(AIOGitHubAPIRatelimitException):
        await client.post("/")


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
