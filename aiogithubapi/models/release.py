"""GitHub release data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase
from .reaction import GitHubReactionModel
from .user import GitHubBaseUserModel


class GitHubReleaseAssetModel(GitHubDataModelBase):
    """Representation of a GitHub release asset."""

    url: str | None = None
    id: int | None = None
    name: str | None = None
    label: str | None = None
    uploader: GitHubBaseUserModel | None = None
    content_type: str | None = None
    state: str | None = None
    size: int | None = None
    download_count: int = None
    created_at: str = None
    updated_at: str = None
    browser_download_url: str = None

    def _generate_uploader(self, data: Dict[str, Any] | None) -> GitHubBaseUserModel:
        """Generate uploader data."""
        return GitHubBaseUserModel(data) if data else None


class GitHubReleaseModel(GitHubDataModelBase):
    """GitHub release data class."""

    url: str | None = None
    assets_url: str | None = None
    upload_url: str | None = None
    html_url: str | None = None
    id: int | None = None
    author: GitHubBaseUserModel | None = None
    tag_name: str | None = None
    target_commitish: str | None = None
    name: str | None = None
    draft: bool | None = None
    prerelease: bool | None = None
    created_at: str | None = None
    published_at: str | None = None
    assets: list[dict] | None = None
    tarball_url: str | None = None
    zipball_url: str | None = None
    body: str | None = None
    reactions: GitHubReactionModel | None = None
    mentions_count: int | None = None

    def _generate_author(self, data: dict) -> GitHubBaseUserModel:
        """Generate author data."""
        return GitHubBaseUserModel(data)

    def _generate_assets(self, data: list[Dict[str, Any]]) -> dict:
        """Generate assets data."""
        return [GitHubReleaseAssetModel(asset) for asset in data or []]

    def _generate_reactions(self, data: dict) -> GitHubReactionModel:
        """Generate reactions data."""
        return GitHubReactionModel(data)
