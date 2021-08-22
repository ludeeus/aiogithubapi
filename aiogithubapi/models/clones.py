"""GitHub clones data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase


class _Clone(GitHubDataModelBase):
    """GitHub clone data."""

    timestamp: str | None = None
    count: int | None = None
    uniques: int | None = None


class GitHubClonesModel(GitHubDataModelBase):
    """GitHub clones data class."""

    count: int | None = None
    uniques: int | None = None
    clones: list[_Clone] | None = None

    def _generate_clones(self, data: list[Dict[str, Any]]) -> list[_Clone]:
        """Generate GitHubClonesModel from list of dicts."""
        return [_Clone(clone) for clone in data or []]
