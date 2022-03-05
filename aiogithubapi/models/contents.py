"""GitHub contents data class."""
from __future__ import annotations

from pydantic import BaseModel


class GitHubContentsModel(BaseModel):
    """GitHub contents data class."""

    type: str
    encoding: str | None
    size: int
    name: str
    path: str
    content: str | None
    sha: str
    url: str
    git_url: str
    html_url: str
    download_url: str | None
