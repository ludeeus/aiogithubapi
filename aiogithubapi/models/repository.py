"""GitHub response data class."""
from __future__ import annotations

from typing import Any, Dict

from .base import GitHubDataModelBase
from .license import GitHubLicenseModel
from .organization import GitHubOrganizationModel
from .owner import GitHubOwnerModel
from .permissions import GitHubPermissionsModel


class GitHubRepositoryModel(GitHubDataModelBase):
    """GitHub repository data class."""

    archive_url: str | None = None
    allow_squash_merge: bool | None = None
    allow_merge_commit: bool | None = None
    allow_rebase_merge: bool | None = None
    allow_auto_merge: bool | None = None
    delete_branch_on_merge: bool | None = None
    archived: bool | None = None
    assignees_url: str | None = None
    blobs_url: str | None = None
    branches_url: str | None = None
    clone_url: str | None = None
    collaborators_url: str | None = None
    comments_url: str | None = None
    commits_url: str | None = None
    compare_url: str | None = None
    contents_url: str | None = None
    contributors_url: str | None = None
    created_at: str | None = None
    default_branch: str | None = None
    deployments_url: str | None = None
    description: str | None = None
    disabled: bool | None = None
    downloads_url: str | None = None
    events_url: str | None = None
    fork: bool | None = None
    forks_count: int | None = None
    forks_url: str | None = None
    forks: int | None = None
    full_name: str | None = None
    git_commits_url: str | None = None
    git_refs_url: str | None = None
    git_tags_url: str | None = None
    git_url: str | None = None
    has_downloads: bool | None = None
    has_issues: bool | None = None
    has_pages: bool | None = None
    has_projects: bool | None = None
    has_wiki: bool | None = None
    homepage: str | None = None
    hooks_url: str | None = None
    html_url: str | None = None
    id: int | None = None
    issue_comment_url: str | None = None
    issue_events_url: str | None = None
    issues_url: str | None = None
    keys_url: str | None = None
    labels_url: str | None = None
    language: str | None = None
    languages_url: str | None = None
    license: GitHubLicenseModel | None = None
    merges_url: str | None = None
    milestones_url: str | None = None
    mirror_url: str | None = None
    name: str | None = None
    network_count: int | None = None
    node_id: str | None = None
    notifications_url: str | None = None
    open_issues_count: int | None = None
    open_issues: int | None = None
    organization: GitHubOrganizationModel | None = None
    owner: GitHubOwnerModel | None = None
    permissions: GitHubPermissionsModel | None = None
    private: bool | None = None
    pulls_url: str | None = None
    pushed_at: str | None = None
    releases_url: str | None = None
    size: int | None = None
    ssh_url: str | None = None
    stargazers_count: int | None = None
    stargazers_url: str | None = None
    statuses_url: str | None = None
    subscribers_count: int | None = None
    subscribers_url: str | None = None
    subscription_url: str | None = None
    svn_url: str | None = None
    tags_url: str | None = None
    teams_url: str | None = None
    temp_clone_token: str | None = None
    topics: list[str] | None = None
    trees_url: str | None = None
    updated_at: str | None = None
    url: str | None = None
    watchers_count: int | None = None
    watchers: int | None = None

    def _generate_license(self, data: Dict[str, Any] | None) -> GitHubLicenseModel:
        """Generate a license model from a dictionary."""
        return GitHubLicenseModel(data) if data else None

    def _generate_owner(self, data: Dict[str, Any] | None) -> GitHubOwnerModel:
        """Generate an owner model from a dictionary."""
        return GitHubOwnerModel(data) if data else None

    def _generate_permissions(self, data: Dict[str, Any] | None) -> GitHubPermissionsModel:
        """Generate a permissions model from a dictionary."""
        return GitHubPermissionsModel(data)

    def _generate_organization(self, data: Dict[str, Any] | None) -> GitHubOrganizationModel:
        """Generate an organization model from a dictionary."""
        return GitHubOrganizationModel(data)
