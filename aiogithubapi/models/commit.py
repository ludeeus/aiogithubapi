"""GitHub commit data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase
from .user import GitHubUserModel


class _Author(GitHubDataModelBase):
    """Internal entry."""

    name: str | None = None
    email: str | None = None
    date: str | None = None


class _Committer(_Author):
    """Internal entry."""


class _Tree(GitHubDataModelBase):
    """Internal entry."""

    sha: str | None = None
    url: str | None = None


class _Verification(GitHubDataModelBase):
    """Internal entry."""

    verified: bool | None = None
    reason: str | None = None
    signature: str | None = None
    payload: str | None = None


class _Parents(GitHubDataModelBase):
    """Internal entry."""

    sha: str | None = None
    url: str | None = None
    html_url: str | None = None


class _Commit(GitHubDataModelBase):
    """Internal entry."""

    author: _Author | None = None
    committer: _Committer | None = None
    message: str | None = None
    tree: _Tree | None = None
    url: str | None = None
    comment_count: int | None = None
    verification: _Verification | None = None

    def _generate_author(self, data: Dict[str, Any] | None) -> _Author:
        """Generate author data."""
        return _Author(data) if data else None

    def _generate_committer(self, data: Dict[str, Any] | None) -> _Committer:
        """Generate committer data."""
        return _Committer(data) if data else None

    def _generate_tree(self, data: Dict[str, Any] | None) -> _Tree:
        """Generate tree data."""
        return _Tree(data) if data else None

    def _generate_verification(self, data: Dict[str, Any] | None) -> _Verification:
        """Generate verification data."""
        return _Verification(data) if data else None


class GitHubCommitModel(GitHubDataModelBase):
    """GitHub commit data class."""

    sha: str | None = None
    commit: _Commit | None = None
    url: str | None = None
    html_url: str | None = None
    comments_url: str | None = None
    author: GitHubUserModel | None = None
    committer: GitHubUserModel | None = None
    parents: list[_Parents] | None = None

    def _generate_commit(self, data: Dict[str, Any] | None) -> _Commit:
        """Generate commit data."""
        return _Commit(data) if data else None

    def _generate_author(self, data: Dict[str, Any] | None) -> GitHubUserModel:
        """Generate author data."""
        return GitHubUserModel(data) if data else None

    def _generate_committer(self, data: Dict[str, Any] | None) -> GitHubUserModel:
        """Generate committer data."""
        return GitHubUserModel(data) if data else None
