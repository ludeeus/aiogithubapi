"""GitHub label data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class GitHubLabelModel(GitHubDataModelBase):
    """GitHub label data class."""

    color: str | None = None
    default: bool | None = None
    description: str | None = None
    id: int | None = None
    name: str | None = None
    url: str | None = None
