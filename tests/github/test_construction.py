"""Construction tests for the main class."""
# pylint: disable=protected-access,missing-function-docstring
from __future__ import annotations

from unittest.mock import patch

import aiohttp
import pytest

from aiogithubapi import GitHubAPI

from tests.common import TOKEN


@pytest.mark.asyncio
async def test_session_creation():
    github = GitHubAPI()
    assert github._session
    assert isinstance(github._session, aiohttp.ClientSession)

    assert not github._session.closed
    await github.close_session()
    assert github._session.closed


@pytest.mark.asyncio
async def test_session_pass():
    async with aiohttp.ClientSession() as session:
        github = GitHubAPI(session=session)
        assert github._session is session


@pytest.mark.asyncio
async def test_session_creation_with_enter():
    async with GitHubAPI() as github:
        assert github._session
        assert isinstance(github._session, aiohttp.ClientSession)
        assert not github._session.closed

    assert github._session.closed


@pytest.mark.asyncio
async def test_token():
    assert GitHubAPI()._client._base_request_data.token is None
    assert GitHubAPI(token=TOKEN)._client._base_request_data.token == TOKEN
    with patch("os.environ", {"GITHUB_TOKEN": TOKEN}):
        assert GitHubAPI()._client._base_request_data.token == TOKEN
