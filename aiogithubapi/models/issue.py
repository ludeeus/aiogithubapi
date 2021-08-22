"""GitHub issue data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase
from .label import GitHubLabelModel
from .milestone import GitHubMilestoneModel
from .user import GitHubUserModel


class _PullRequest(GitHubDataModelBase):
    """GitHub pull_request data model."""

    url: str | None = None
    html_url: str | None = None
    diff_url: str | None = None
    patch_url: str | None = None


class GitHubIssueModel(GitHubDataModelBase):
    """GitHub issue data class."""

    active_lock_reason: str | None = None
    author_association: str | None = None
    body: str | None = None
    closed_at: str | None = None
    closed_by: GitHubUserModel | None = None
    comments_url: str | None = None
    comments: int | None = None
    created_at: str | None = None
    events_url: str | None = None
    html_url: str | None = None
    id: int | None = None
    labels_url: str | None = None
    locked: bool | None = None
    milestone: GitHubMilestoneModel | None = None
    number: int | None = None
    repository_url: str | None = None
    state: str | None = None
    title: str | None = None
    updated_at: str | None = None
    url: str | None = None
    pull_request: _PullRequest | None = None
    assignees: list[GitHubUserModel] | None = None
    assignee: GitHubUserModel | None = None
    user: GitHubUserModel | None = None
    labels: list[GitHubLabelModel] | None = None

    @property
    def is_pull_request(self) -> bool:
        """Return True if issue is a pull request."""
        return self.pull_request is not None

    def _generate_labels(self, data: list[Dict[str, Any]]) -> list[GitHubLabelModel]:
        """Generate GitHubLabelModel list from data."""
        return [GitHubLabelModel(label) for label in data or []]

    def _generate_assignees(self, data: list[Dict[str, Any]]) -> list[GitHubUserModel]:
        """Generate GitHubUserModel list from data."""
        return [GitHubUserModel(user) for user in data or []]

    def _generate_assignee(self, data: Dict[str, Any] | None) -> GitHubUserModel:
        """Generate GitHubUserModel from data."""
        return GitHubUserModel(data) if data else None

    def _generate_milestone(self, data: Dict[str, Any] | None) -> "GitHubMilestoneModel":
        """Generate GitHubMilestoneModel from data."""
        return GitHubMilestoneModel(data) if data else None

    def _generate_closed_by(self, data: Dict[str, Any] | None) -> GitHubUserModel:
        """Generate GitHubUserModel from data."""
        return GitHubUserModel(data) if data else None

    def _generate_pull_request(self, data: Dict[str, Any] | None) -> _PullRequest:
        """Generate GitHubPullRequestModel from data."""
        return _PullRequest(data) if data else None
