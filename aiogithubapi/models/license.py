"""GitHub license data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class GitHubLicenseModel(GitHubDataModelBase):
    """GitHub license data class."""

    key: str | None = None
    name: str | None = None
    spdx_id: str | None = None
    url: str | None = None
