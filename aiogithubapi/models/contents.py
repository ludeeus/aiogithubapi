"""GitHub contents data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class GitHubContentsModel(GitHubDataModelBase):
    """GitHub contents data class."""

    type: str | None = None
    encoding: str | None = None
    size: int | None = None
    name: str | None = None
    path: str | None = None
    content: str | None = None
    sha: str | None = None
    url: str | None = None
    git_url: str | None = None
    html_url: str | None = None
    download_url: str | None = None
