"""Test events namespace."""
# pylint: disable=missing-docstring
import asyncio
from unittest.mock import AsyncMock, patch

import pytest
import aiohttp

from aiogithubapi import GitHubAPI, GitHubEventModel

from tests.common import TEST_REPOSITORY_NAME, TOKEN, MockedRequests, MockResponse


@pytest.fixture()
async def wait_mock():
    async def _mocker(_, __):
        await asyncio.sleep(0)

    with patch("aiogithubapi.namespaces.events._GitHubEventsBaseNamespace._wait", _mocker):
        yield


@pytest.mark.asyncio
async def test_subscription(github_api: GitHubAPI, mock_requests: MockedRequests):
    tasks_before = asyncio.all_tasks(github_api._client._loop)  # This includes the test task
    assert len(tasks_before) == 1

    event_callback_mock = AsyncMock()

    subscription_id = await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME, event_callback=event_callback_mock
    )

    assert subscription_id in github_api.repos.events._subscriptions
    while not event_callback_mock.called:
        await asyncio.sleep(0)

    event: GitHubEventModel = event_callback_mock.call_args[0][0]
    assert event.type == "PushEvent"

    assert len(asyncio.all_tasks(github_api._client._loop) - tasks_before) == 1

    tasks = github_api.repos.events.unsubscribe(subscription_id=subscription_id)
    await asyncio.wait(tasks)
    assert not github_api.repos.events._subscriptions
    assert len(asyncio.all_tasks(github_api._client._loop) - tasks_before) == 0


@pytest.mark.asyncio
async def test_stopping_all_subscriptions(github_api: GitHubAPI, mock_requests: MockedRequests):
    tasks_before = asyncio.all_tasks(github_api._client._loop)  # This includes the test task
    assert len(tasks_before) == 1

    event_callback_mock = AsyncMock()

    subscription_id_1 = await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME, event_callback=event_callback_mock
    )
    subscription_id_2 = await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME, event_callback=event_callback_mock
    )

    assert subscription_id_1 in github_api.repos.events._subscriptions
    assert subscription_id_2 in github_api.repos.events._subscriptions
    while not event_callback_mock.called:
        await asyncio.sleep(0)

    event: GitHubEventModel = event_callback_mock.call_args[0][0]
    assert event.type == "PushEvent"

    assert len(asyncio.all_tasks(github_api._client._loop) - tasks_before) == 2

    await github_api.repos.events.unsubscribe_all()
    assert len(asyncio.all_tasks(github_api._client._loop) - tasks_before) == 0


@pytest.mark.asyncio
async def test_stopping_all_subscriptions_async_with(
    event_loop: asyncio.AbstractEventLoop,
    client_session: aiohttp.ClientSession,
    mock_requests: MockedRequests,
):
    tasks_before = asyncio.all_tasks(event_loop)  # This includes the test task
    assert len(tasks_before) == 1

    event_callback_mock = AsyncMock()

    async with GitHubAPI(token=TOKEN, session=client_session) as github_api:
        subscription_id = await github_api.repos.events.subscribe(
            TEST_REPOSITORY_NAME, event_callback=event_callback_mock
        )

        assert subscription_id in github_api.repos.events._subscriptions
        while not event_callback_mock.called:
            await asyncio.sleep(0)

        event: GitHubEventModel = event_callback_mock.call_args[0][0]
        assert event.type == "PushEvent"

        assert len(asyncio.all_tasks(event_loop) - tasks_before) == 1

    assert len(asyncio.all_tasks(event_loop) - tasks_before) == 0


@pytest.mark.asyncio
async def test_subscription_exceptions_not_modified(
    github_api: GitHubAPI,
    mock_response: MockResponse,
    mock_requests: MockedRequests,
    wait_mock: None,
):
    mock_requests.clear()
    event_callback_mock = AsyncMock()
    error_callback_mock = AsyncMock()

    mock_response.mock_status = 304

    subscription_id = await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME,
        event_callback=event_callback_mock,
        error_callback=error_callback_mock,
    )

    while mock_requests.called < 10:
        await asyncio.sleep(0)

    assert subscription_id in github_api.repos.events._subscriptions
    assert not event_callback_mock.called
    assert not error_callback_mock.called

    github_api.repos.events.unsubscribe()
    assert not github_api.repos.events._subscriptions


@pytest.mark.asyncio
async def test_subscription_exceptions_not_found(
    github_api: GitHubAPI,
    mock_response: MockResponse,
    wait_mock: None,
):
    event_callback_mock = AsyncMock()
    error_callback_mock = AsyncMock()

    mock_response.mock_status = 404

    await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME,
        event_callback=event_callback_mock,
        error_callback=error_callback_mock,
    )

    while not error_callback_mock.called:
        await asyncio.sleep(0)

    assert not event_callback_mock.called
    assert error_callback_mock.called

    github_api.repos.events.unsubscribe()
    assert not github_api.repos.events._subscriptions


@pytest.mark.asyncio
async def test_subscription_exception(
    github_api: GitHubAPI,
    mock_response: MockResponse,
    mock_requests: MockedRequests,
    wait_mock: None,
):
    event_callback_mock = AsyncMock()
    error_callback_mock = AsyncMock()

    mock_response.mock_status = 400

    await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME,
        event_callback=event_callback_mock,
        error_callback=error_callback_mock,
    )

    while not error_callback_mock.called:
        await asyncio.sleep(0)

    while mock_requests.called < 10:
        await asyncio.sleep(0)

    assert not event_callback_mock.called
    assert error_callback_mock.called

    github_api.repos.events.unsubscribe()
    assert not github_api.repos.events._subscriptions


@pytest.mark.asyncio
async def test_subscription_exception_in_handler(
    github_api: GitHubAPI,
    mock_response: MockResponse,
    wait_mock: None,
):
    event_callback_mock = AsyncMock(side_effect=TypeError)
    error_callback_mock = AsyncMock()

    await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME,
        event_callback=event_callback_mock,
        error_callback=error_callback_mock,
    )

    while not event_callback_mock.called and not error_callback_mock.called:
        await asyncio.sleep(0)

    assert event_callback_mock.called
    assert error_callback_mock.called

    github_api.repos.events.unsubscribe()
    assert not github_api.repos.events._subscriptions
