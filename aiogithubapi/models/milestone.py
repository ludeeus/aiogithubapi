"""GitHub milestone data class."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from .user import GitHubBaseUserModel


class GitHubMilestoneModel(BaseModel):
    """GitHub milestone data class."""

    closed_at: datetime
    closed_issues: int
    created_at: datetime
    description: str | None
    due_on: datetime | None
    html_url: str
    id: int
    labels_url: str
    number: int
    open_issues: int
    state: str
    title: str
    updated_at: datetime
    url: str
    creator: GitHubBaseUserModel
