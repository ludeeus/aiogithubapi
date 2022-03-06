"""GitHub milestone data class."""
from __future__ import annotations

from pydantic import BaseModel

from .user import GitHubBaseUserModel


class GitHubMilestoneModel(BaseModel):
    """GitHub milestone data class."""

    closed_at: str
    closed_issues: int
    created_at: str
    description: str | None
    due_on: str | None
    html_url: str
    id: int
    labels_url: str
    number: int
    open_issues: int
    state: str
    title: str
    updated_at: str
    url: str
    creator: GitHubBaseUserModel
