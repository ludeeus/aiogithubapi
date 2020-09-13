import pytest
import aiohttp
from aiogithubapi import GitHub, GitHubDevice
from aiogithubapi.client import AIOGitHubAPIClient
from tests.const import TOKEN, CLIENT_ID


@pytest.fixture
async def client():
    """Fixture to provide a GitHub client object."""
    async with aiohttp.ClientSession() as session:
        client_obj = AIOGitHubAPIClient(session, TOKEN)
        client_obj.ratelimits.remaining = "1337"
        yield client_obj


@pytest.fixture
async def github(client):
    """Fixture to provide a GitHub object."""
    async with GitHub(TOKEN) as github_obj:
        github_obj.client = client
        yield github_obj


@pytest.fixture
async def github_device():
    """Fixture to provide a GitHub Devlice object."""
    async with GitHubDevice(CLIENT_ID) as github_device_obj:
        yield github_device_obj