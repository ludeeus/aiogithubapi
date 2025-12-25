"""GitHub notification models"""

from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase
from .repository import GitHubRepositoryModel


class _Subject(GitHubDataModelBase):
    """Notification subject."""

    title: str | None = None
    url: str | None = None
    latest_comment_url: str | None = None
    type: str | None = None


class GitHubNotificationModel(GitHubDataModelBase):
    """
    GitHub notification data class.

    https://docs.github.com/en/rest/activity/notifications
    """

    id: str | None = None
    repository: GitHubRepositoryModel | None = None
    subject: _Subject | None = None
    reason: str | None = None
    unread: bool | None = None
    updated_at: str | None = None
    last_read_at: str | None = None
    url: str | None = None
    subscription_url: str | None = None

    def _generate_repository(self, data: Dict[str, Any] | None) -> GitHubRepositoryModel:
        """Generate repository data."""
        return GitHubRepositoryModel(data) if data else None

    def _generate_subject(self, data: Dict[str, Any] | None) -> _Subject:
        """Generate subject data."""
        return _Subject(data) if data else None
