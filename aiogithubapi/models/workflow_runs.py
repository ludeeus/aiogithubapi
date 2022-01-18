"""GitHub workflow runs data class."""
from __future__ import annotations

from typing import Any, Dict

from aiogithubapi.const import Repository

from .base import GitHubDataModelBase


class _WorkflowRun(GitHubDataModelBase):
    """GitHub workflow data."""

    id: int | None = None
    name: str | None = None
    node_id: str | None = None
    head_branch: str | None = None
    head_sha: str | None = None
    run_number: int | None = None
    event: str | None = None
    status: str | None = None
    conclusion: str | None = None
    workflow_id: int | None = None
    url: str | None = None
    html_url: str | None = None
    pull_requests: list[Dict[str, Any]] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    jobs_url: str | None = None
    logs_url: str | None = None
    check_suite_url: str | None = None
    artifacts_url: str | None = None
    cancel_url: str | None = None
    rerun_url: str | None = None
    workflow_url: str | None = None
    head_commit: Dict[str, Any] | None = None
    repository: Repository | None = None
    private: bool | None = None
    head_repository: Repository | None = None


class GitHubWorkflowRunsModel(GitHubDataModelBase):
    """GitHub workflows data class."""

    total_count: int | None = None
    workflow_runs: list[_WorkflowRun] | None = None

    def _generate_workflows(self, data: list[Dict[str, Any]]) -> list[_WorkflowRun]:
        """Generate GitHubWorkflowRunsModel from list of dicts."""
        return [_WorkflowRun(workflow_run) for workflow_run in data or []]
