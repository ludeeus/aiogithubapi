"""GitHub release data class."""
from __future__ import annotations

from pydantic import BaseModel

from .reaction import GitHubReactionModel
from .user import GitHubBaseUserModel


class GitHubReleaseAssetModel(BaseModel):
    """Representation of a GitHub release asset."""

    url: str
    id: int
    name: str
    label: str
    uploader: GitHubBaseUserModel
    content_type: str
    state: str
    size: int
    download_count: int
    created_at: str
    updated_at: str
    browser_download_url: str


class GitHubReleaseModel(BaseModel):
    """GitHub release data class."""

    url: str
    assets_url: str
    upload_url: str
    html_url: str
    id: int
    author: GitHubBaseUserModel
    tag_name: str
    target_commitish: str
    name: str
    draft: bool
    prerelease: bool
    created_at: str
    published_at: str
    assets: list[GitHubReleaseAssetModel]
    tarball_url: str
    zipball_url: str
    body: str
    reactions: GitHubReactionModel | None
    mentions_count: int | None
