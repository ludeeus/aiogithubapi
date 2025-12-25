"""Test notifications namespace."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI
from aiogithubapi.models.notification import GitHubNotificationModel

from tests.common import (
    MockedRequests,
)


@pytest.mark.asyncio
async def test_list_notifications(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.notifications.list()
    assert response.status == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1
    assert isinstance(response.data[0], GitHubNotificationModel)
    assert response.data[0].id == "1"
    assert response.data[0].subject.title == "Greetings"
    assert response.data[0].reason == "subscribed"
    assert response.data[0].unread is True
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/notifications"
