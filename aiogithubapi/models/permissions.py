"""GitHub permissions data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class GitHubPermissionsModel(GitHubDataModelBase):
    """GitHub permissions data class."""

    admin: bool | None = None
    maintain: bool | None = None
    push: bool | None = None
    triage: bool | None = None
    pull: bool | None = None
