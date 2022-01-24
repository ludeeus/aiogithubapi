"""GitHub tag data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class _Commit(GitHubDataModelBase):
    """Representation of a GitHub tag commit."""

    sha: str | None = None
    url: str | None = None


class GitHubTagModel(GitHubDataModelBase):
    """GitHub tag data class."""

    name: str | None = None
    commit: _Commit | None = None
    zipball_url: str | None = None
    tarball_url: str | None = None

    def _generate_commit(self, data: dict) -> _Commit:
        """Generate commit data."""
        return _Commit(data)
