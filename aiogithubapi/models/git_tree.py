"""GitHub git data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase


class GitHubGitTreeEntryModel(GitHubDataModelBase):
    """GitHub git tree entry model."""

    mode: str | None = None
    path: str | None = None
    sha: str | None = None
    size: int | None = None
    type: str | None = None
    url: str | None = None


class GitHubGitTreeModel(GitHubDataModelBase):
    """GitHub git data class."""

    sha: str | None = None
    tree: list[GitHubGitTreeEntryModel] | None = None
    truncated: bool | None = None
    url: str | None = None

    def _generate_tree(self, data: list[Dict[str, Any]]) -> list:
        """Generate tree entries."""
        return [GitHubGitTreeEntryModel(entry) for entry in data or []]
