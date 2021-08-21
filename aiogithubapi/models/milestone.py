"""GitHub milestone data class."""
from __future__ import annotations

from .base import GitHubDataModelBase
from .user import GitHubUserModel


class GitHubMilestoneModel(GitHubDataModelBase):
    """GitHub milestone data class."""

    closed_at: str | None = None
    closed_issues: int | None = None
    created_at: str | None = None
    description: str | None = None
    due_on: str | None = None
    html_url: str | None = None
    id: int | None = None
    labels_url: str | None = None
    number: int | None = None
    open_issues: int | None = None
    state: str | None = None
    title: str | None = None
    updated_at: str | None = None
    url: str | None = None
    creator: GitHubUserModel | None = None

    def _generate_creator(self, data: dict) -> GitHubUserModel:
        """Generate the creator."""
        return GitHubUserModel(data)
