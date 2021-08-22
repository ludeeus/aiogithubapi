"""GitHub reaction data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class GitHubReactionModel(GitHubDataModelBase):
    """GitHub reaction data class."""

    _log_missing: bool = False

    url: str | None = None
    total_count: int | None = None
    thumbs_up: int | None = None
    thumbs_down: int | None = None
    laugh: int | None = None
    hooray: int | None = None
    confused: int | None = None
    heart: int | None = None
    rocket: int | None = None
    eyes: int | None = None

    def __post_init__(self):
        """Initialize attributes."""
        self.thumbs_up = self._raw_data.get("+1", 0)
        self.thumbs_down = self._raw_data.get("-1", 0)
