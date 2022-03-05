"""Test events namespace."""
# pylint: disable=missing-docstring
import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from aiogithubapi import GitHubAPI, GitHubEventModel, GitHubRepositoryModel

from tests.common import TEST_REPOSITORY_NAME, MockedRequests, MockResponse


@pytest.fixture()
async def wait_mock():
    async def _mocker(_, __):
        await asyncio.sleep(0)

    with patch("aiogithubapi.namespaces.events._GitHubEventsBaseNamespace._wait", _mocker):
        yield


@pytest.mark.asyncio
async def test_subscription(github_api: GitHubAPI, mock_requests: MockedRequests):
    event_callback_mock = AsyncMock()

    subscription_id = await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME, event_callback=event_callback_mock
    )

    assert subscription_id in github_api.repos.events._subscriptions
    while not event_callback_mock.called:
        await asyncio.sleep(0)

    event: GitHubEventModel = event_callback_mock.call_args[0][0]
    assert event.type == "PushEvent"

    github_api.repos.events.unsubscribe(subscription_id=subscription_id)
    assert not github_api.repos.events._subscriptions


@pytest.mark.asyncio
async def test_subscription_exceptions_not_modified(
    github_api: GitHubAPI,
    mock_response: MockResponse,
    mock_requests: MockedRequests,
    wait_mock: None,
):
    event_callback_mock = AsyncMock()
    error_callback_mock = AsyncMock()

    mock_response.mock_status = 304

    subscription_id = await github_api.repos.events.subscribe(
        TEST_REPOSITORY_NAME,
        event_callback=event_callback_mock,
        error_callback=error_callback_mock,
    )

    while not mock_requests.called:
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
