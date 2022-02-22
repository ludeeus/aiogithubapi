"""GitHub Activity event models"""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase


class _Actor(GitHubDataModelBase):
    """Internal entry."""

    id: str | None = None
    login: str | None = None
    display_login: str | None = None
    gravatar_id: str | None = None
    url: str | None = None
    avatar_url: str | None = None


class _Repo(GitHubDataModelBase):
    """Internal entry."""

    id: str | None = None
    name: str | None = None
    url: str | None = None


class _CommitAuthor(GitHubDataModelBase):
    """Internal entry."""

    id: str | None = None
    login: str | None = None
    display_login: str | None = None
    gravatar_id: str | None = None
    url: str | None = None
    avatar_url: str | None = None


class _Commit(GitHubDataModelBase):
    """Internal entry."""

    sha: str | None = None
    author: _CommitAuthor | None = None
    message: str | None = None
    distinct: bool | None = None
    url: str | None = None

    def _generate_author(self, data: Dict[str, Any] | None) -> _CommitAuthor:
        """Generate author data."""
        return _CommitAuthor(data) if data else None


class GitHubEventModel(GitHubDataModelBase):
    """GitHub base event data class."""

    id: str | None = None
    type: str | None = None
    actor: _Actor | None = None
    repo: _Repo | None = None
    payload: Dict[str, Any] | None = None
    public: bool | None = None
    created_at: str | None = None

    def _generate_actor(self, data: Dict[str, Any] | None) -> _Actor:
        """Generate actor data."""
        return _Actor(data) if data else None

    def _generate_repo(self, data: Dict[str, Any] | None) -> _Repo:
        """Generate repo data."""
        return _Repo(data) if data else None
