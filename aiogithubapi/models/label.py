"""GitHub label data class."""
from __future__ import annotations

from pydantic import BaseModel


class GitHubLabelModel(BaseModel):
    """GitHub label data class."""

    color: str
    default: bool
    description: str
    id: int
    name: str
    url: str
