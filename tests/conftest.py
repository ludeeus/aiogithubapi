"""Test fixtures and configuration."""
# pylint: disable=redefined-outer-name,protected-access
from datetime import datetime
import logging
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest

from aiogithubapi import GitHub, GitHubAPI, GitHubDevice, GitHubDeviceAPI
from aiogithubapi.client import AIOGitHubAPIClient
from aiogithubapi.const import PROJECT_NAME

from .common import CLIENT_ID, TOKEN

from tests.common import MockedRequests, MockResponse

logging.basicConfig(level=logging.ERROR)
logging.getLogger(PROJECT_NAME).setLevel(logging.DEBUG)


@pytest.fixture()
def asyncio_sleep():
    """Mock asyncio.sleep."""
    with patch("asyncio.sleep", new=AsyncMock()) as mock_sleep:
        yield mock_sleep


@pytest.fixture()
def mock_requests():
    """Return a new mock request instance."""
    yield MockedRequests()


@pytest.fixture()
def response():
    """Return a new mock response instance."""
    yield MockResponse()


@pytest.fixture()
def mock_response():
    """Return a new mock response instance."""
    yield MockResponse()


@pytest.fixture(autouse=True)
async def client_session(mock_response, mock_requests):
    """Mock our the request part of the client session."""

    async def _mocked_request(*args, **kwargs):
        if len(args) > 2:
            mock_response.mock_endpoint = args[2].split(".com/")[-1]
            mock_requests.add({"method": args[1], "url": args[2], **kwargs})
        else:
            mock_response.mock_endpoint = args[1].split(".com/")[-1]
            mock_requests.add({"method": args[0], "url": args[1], **kwargs})
        return mock_response

    async with aiohttp.ClientSession() as session:
        mock_requests.clear()
        session._request = _mocked_request  # pylint: disable=protected-access
        yield session


@pytest.fixture
async def client(client_session):
    """Fixture to provide a GitHub client object."""
    client_obj = AIOGitHubAPIClient(client_session, TOKEN)
    yield client_obj


@pytest.fixture
async def github(client, client_session):
    """Fixture to provide a GitHub object."""
    async with GitHub(TOKEN, session=client_session) as github_obj:
        github_obj.client = client
        yield github_obj


@pytest.fixture
async def github_api(client_session, mock_response):
    """Fixture to provide a GitHub object."""
    mock_response.throw_on_file_error = True
    async with GitHubAPI(
        token=TOKEN,
        session=client_session,
    ) as github_obj:
        yield github_obj


@pytest.fixture
async def github_device(client_session):
    """Fixture to provide a GitHub Devlice object."""
    async with GitHubDevice(CLIENT_ID, session=client_session) as github_device_obj:
        yield github_device_obj


@pytest.fixture
async def github_device_api(client_session):
    """Fixture to provide a GitHub Devlice object."""
    async with GitHubDeviceAPI(
        CLIENT_ID,
        session=client_session,
    ) as github_device_obj:
        github_device_obj._interval = 1
        github_device_obj._expires = datetime.timestamp(datetime.now()) + 900
        yield github_device_obj
