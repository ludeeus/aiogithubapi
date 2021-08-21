"""GitHub views data class."""
from __future__ import annotations

from typing import Any

from .base import GitHubDataModelBase


class _View(GitHubDataModelBase):
    """GitHub view data."""

    timestamp: str | None = None
    count: int | None = None
    uniques: int | None = None


class GitHubViewsModel(GitHubDataModelBase):
    """GitHub views data class."""

    count: int | None = None
    uniques: int | None = None
    views: list[_View] | None = None

    def _generate_views(self, data: list[dict[str, Any]]) -> list[_View]:
        """Generate views from list of dicts."""
        return [_View(view) for view in data or []]
