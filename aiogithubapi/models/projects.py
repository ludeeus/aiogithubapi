"""GitHub projects model."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase
from .user import GitHubBaseUserModel


class GitHubProjectModel(GitHubDataModelBase):
    """GitHub project model."""

    owner_url: str | None = None
    url: str | None = None
    html_url: str | None = None
    columns_url: str | None = None
    id: int | None = None
    node_id: str | None = None
    name: str | None = None
    body: str | None = None
    number: int | None = None
    state: str | None = None
    creator: GitHubBaseUserModel | None = None
    created_at: str | None = None
    updated_at: str | None = None

    def _generate_creator(self, data: Dict[str, Any] | None) -> GitHubBaseUserModel:
        """Generate GitHub user creator model."""
        return GitHubBaseUserModel(data) if data else None
