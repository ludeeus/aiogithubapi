"""GitHub commit data class."""
from __future__ import annotations

from pydantic import BaseModel

from .user import GitHubBaseUserModel


class _Author(BaseModel):
    """Internal entry."""

    name: str
    email: str
    date: str


class _Committer(_Author):
    """Internal entry."""


class _Tree(BaseModel):
    """Internal entry."""

    sha: str
    url: str


class _Verification(BaseModel):
    """Internal entry."""

    verified: bool
    reason: str
    signature: str | None
    payload: str | None


class _Parents(BaseModel):
    """Internal entry."""

    sha: str
    url: str
    html_url: str


class _Commit(BaseModel):
    """Internal entry."""

    author: _Author
    committer: _Committer
    message: str
    tree: _Tree
    url: str
    comment_count: int
    verification: _Verification


class GitHubCommitModel(BaseModel):
    """GitHub commit data class."""

    sha: str
    commit: _Commit
    url: str
    html_url: str
    comments_url: str
    author: GitHubBaseUserModel
    committer: GitHubBaseUserModel
    parents: list[_Parents]
