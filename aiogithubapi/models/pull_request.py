"""GitHub pull_request data model."""
from __future__ import annotations

from .issue import GitHubIssueModel


class GitHubPullRequestModel(GitHubIssueModel):
    """GitHub pull_request data model."""

    diff_url: str | None = None
    patch_url: str | None = None
    issue_url: str | None = None
    merged_at: str | None = None
    merge_commit_sha: str | None = None
    requested_reviewers: list[dict] | None = None
    requested_teams: list[dict] | None = None
    draft: bool | None = None
    head: dict | None = None
    base: dict | None = None
    auto_merge: bool | None = None
    commits_url: str | None = None
    review_comments_url: str | None = None
    review_comment_url: str | None = None
    statuses_url: str | None = None
