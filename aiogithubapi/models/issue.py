"""GitHub issue data class."""
from __future__ import annotations

from pydantic import BaseModel

from .label import GitHubLabelModel
from .milestone import GitHubMilestoneModel
from .user import GitHubBaseUserModel


class _PullRequest(BaseModel):
    """GitHub pull_request data model."""

    url: str
    html_url: str
    diff_url: str
    patch_url: str


class GitHubIssueModel(BaseModel):
    """GitHub issue data class."""

    active_lock_reason: str | None
    author_association: str
    body: str
    closed_at: str
    closed_by: GitHubBaseUserModel
    comments_url: str
    comments: int
    created_at: str
    events_url: str
    html_url: str
    id: int
    labels_url: str
    locked: bool
    milestone: GitHubMilestoneModel
    number: int
    repository_url: str
    state: str
    title: str
    updated_at: str
    url: str
    pull_request: _PullRequest | None
    assignees: list[GitHubBaseUserModel]
    assignee: GitHubBaseUserModel | None
    user: GitHubBaseUserModel
    labels: list[GitHubLabelModel]

    @property
    def is_pull_request(self) -> bool:
        """Return True if issue is a pull request."""
        return self.pull_request is not None
