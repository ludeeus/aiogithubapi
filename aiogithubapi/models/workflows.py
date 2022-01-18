"""GitHub workflows data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase


class _Workflow(GitHubDataModelBase):
    """GitHub workflow data."""

    id: int | None = None
    node_id: str | None = None
    name: str | None = None
    path: str | None = None
    path: str | None = None
    state: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    url: str | None = None
    html_url: str | None = None
    badge_url: str | None = None


class GitHubWorkflowsModel(GitHubDataModelBase):
    """GitHub workflows data class."""

    total_count: int | None = None
    workflows: list[_Workflow] | None = None

    def _generate_workflows(self, data: list[Dict[str, Any]]) -> list[_Workflow]:
        """Generate GitHubWorkflowsModel from list of dicts."""
        return [_Workflow(clone) for clone in data or []]
