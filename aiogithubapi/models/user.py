"""GitHub user models data class."""
from __future__ import annotations

from pydantic import BaseModel


class GitHubBaseUserModel(BaseModel):
    """GitHub base user data class."""

    avatar_url: str
    events_url: str
    followers_url: str
    following_url: str
    gists_url: str
    gravatar_id: str
    html_url: str
    id: int
    login: str
    organizations_url: str
    received_events_url: str
    repos_url: str
    site_admin: bool
    starred_url: str
    subscriptions_url: str
    type: str
    url: str


class GitHubUserModel(GitHubBaseUserModel):
    """GitHub user data class."""

    bio: str
    blog: str
    company: str
    created_at: str
    email: str
    followers: int
    following: int
    hireable: bool
    location: str
    name: str
    public_gists: int
    public_repos: int
    twitter_username: str
    updated_at: str


class GitHubAuthenticatedUserModel(GitHubUserModel):
    """GitHub authenticated user data class."""

    collaborators: int
    disk_usage: int
    owned_private_repos: int
    plan: GitHubUserPlanModel
    private_gists: int
    total_private_repos: int
    two_factor_authentication: bool


class GitHubUserPlanModel(BaseModel):
    """GitHub user plan data class."""

    collaborators: int
    name: str
    private_repos: int
    space: int
