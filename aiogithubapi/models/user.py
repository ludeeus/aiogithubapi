"""GitHub user models data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase


class GitHubBaseUserModel(GitHubDataModelBase):
    """GitHub base user data class."""

    avatar_url: str | None = None
    events_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    html_url: str | None = None
    id: int | None = None
    login: str | None = None
    organizations_url: str | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    type: str | None = None
    url: str | None = None


class GitHubUserModel(GitHubBaseUserModel):
    """GitHub user data class."""

    bio: str | None = None
    blog: str | None = None
    company: str | None = None
    created_at: str | None = None
    email: str | None = None
    followers: int | None = None
    following: int | None = None
    hireable: bool | None = None
    location: str | None = None
    name: str | None = None
    public_gists: int | None = None
    public_repos: int | None = None
    twitter_username: str | None = None
    updated_at: str | None = None


class GitHubAuthenticatedUserModel(GitHubUserModel):
    """GitHub authenticated user data class."""

    collaborators: int | None = None
    disk_usage: int | None = None
    owned_private_repos: int | None = None
    plan: GitHubUserPlanModel | None = None
    private_gists: int | None = None
    total_private_repos: int | None = None
    two_factor_authentication: bool | None = None

    def _generate_plan(self, data: Dict[str, Any] | None) -> GitHubUserPlanModel:
        """Generate GitHub user plan model."""
        return GitHubUserPlanModel(data) if data else None


class GitHubUserPlanModel(GitHubDataModelBase):
    """GitHub user plan data class."""

    collaborators: int | None = None
    name: str | None = None
    private_repos: int | None = None
    space: int | None = None
