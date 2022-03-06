"""GitHub organization model."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase


class _Plan(GitHubDataModelBase):
    """GitHub organization plan data model."""

    name: str | None = None
    space: int | None = None
    private_repos: int | None = None
    filled_seats: int | None = None
    seats: int | None = None


class GitHubOrganizationModel(GitHubDataModelBase):
    """GitHub organization model."""

    login: str | None = None
    id: int | None = None
    node_id: str | None = None
    url: str | None = None
    repos_url: str | None = None
    events_url: str | None = None
    hooks_url: str | None = None
    issues_url: str | None = None
    members_url: str | None = None
    public_members_url: str | None = None
    avatar_url: str | None = None
    description: str | None = None
    name: str | None = None
    company: str | None = None
    blog: str | None = None
    location: str | None = None
    email: str | None = None
    twitter_username: str | None = None
    is_verified: bool | None = None
    has_organization_projects: bool | None = None
    has_repository_projects: bool | None = None
    public_repos: int | None = None
    public_gists: int | None = None
    followers: int | None = None
    following: int | None = None
    html_url: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    type: str | None = None
    total_private_repos: int | None = None
    owned_private_repos: int | None = None
    private_gists: int | None = None
    disk_usage: int | None = None
    collaborators: int | None = None
    billing_email: str | None = None
    plan: _Plan | None = None
    default_repository_permission: str | None = None
    members_can_create_repositories: bool | None = None
    two_factor_requirement_enabled: bool | None = None
    members_allowed_repository_creation_type: str | None = None
    members_can_create_public_repositories: bool | None = None
    members_can_create_private_repositories: bool | None = None
    members_can_create_internal_repositories: bool | None = None
    members_can_create_pages: bool | None = None
    members_can_fork_private_repositories: bool | None = None

    def _generate_plan(self, data: Dict[str, Any]) -> _Plan:
        """Generate GitHubLabelModel list from data."""
        return _Plan(data) if data else None


class GitHubOrganizationMinimalModel(GitHubDataModelBase):
    """GitHub organization minimal model."""

    login: str | None = None
    id: int | None = None
    node_id: str | None = None
    url: str | None = None
    repos_url: str | None = None
    events_url: str | None = None
    hooks_url: str | None = None
    issues_url: str | None = None
    members_url: str | None = None
    public_members_url: str | None = None
    avatar_url: str | None = None
    description: str | None = None
