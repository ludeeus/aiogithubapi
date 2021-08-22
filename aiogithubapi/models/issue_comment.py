"""GitHub issue_comment data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase
from .user import GitHubUserModel


class GitHubIssueCommentModel(GitHubDataModelBase):
    """GitHub issue_comment data class."""

    author_association: str | None = None
    body: str | None = None
    created_at: str | None = None
    html_url: str | None = None
    id: int | None = None
    issue_url: str | None = None
    updated_at: str | None = None
    url: str | None = None
    user: GitHubUserModel | None = None

    def _generate_user(self, data: Dict[str, Any] | None) -> GitHubUserModel:
        """Generate GitHubUserModel."""
        return GitHubUserModel(data) if data else None
