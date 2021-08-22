"""GitHub rate limit data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase


class GitHubRateLimitResourceModel(GitHubDataModelBase):
    """GitHub rate limit resource data class."""

    limit: int | None = None
    used: int | None = None
    remaining: int | None = None
    reset: int | None = None


class GitHubRateLimitResourcesModel(GitHubDataModelBase):
    """GitHub rate limit resources data class."""

    core: GitHubRateLimitResourceModel | None = None
    search: GitHubRateLimitResourceModel | None = None
    graphql: GitHubRateLimitResourceModel | None = None
    integration_manifest: GitHubRateLimitResourceModel | None = None
    source_import: GitHubRateLimitResourceModel | None = None
    code_scanning_upload: GitHubRateLimitResourceModel | None = None

    def _generate_core(self, data: Any) -> GitHubRateLimitResourceModel:
        return GitHubRateLimitResourceModel(data) if data else None

    def _generate_search(self, data: Any) -> GitHubRateLimitResourceModel:
        return GitHubRateLimitResourceModel(data) if data else None

    def _generate_graphql(self, data: Any) -> GitHubRateLimitResourceModel:
        return GitHubRateLimitResourceModel(data) if data else None

    def _generate_integration_manifest(self, data: Any) -> GitHubRateLimitResourceModel:
        return GitHubRateLimitResourceModel(data) if data else None

    def _generate_source_import(self, data: Any) -> GitHubRateLimitResourceModel:
        return GitHubRateLimitResourceModel(data) if data else None

    def _generate_code_scanning_upload(self, data: Any) -> GitHubRateLimitResourceModel:
        return GitHubRateLimitResourceModel(data) if data else None


class GitHubRateLimitModel(GitHubDataModelBase):
    """GitHub rate limit data class."""

    rate: GitHubRateLimitResourceModel | None = None
    resources: GitHubRateLimitResourcesModel | None = None

    def _generate_rate(self, data: Dict[str, Any]) -> GitHubRateLimitResourceModel:
        """Generate rate limit resource model."""
        return GitHubRateLimitResourceModel(data) if data else None

    def _generate_resources(self, data: Dict[str, Any]) -> GitHubRateLimitResourcesModel:
        """Generate rate limit resources model."""
        return GitHubRateLimitResourcesModel(data) if data else None
