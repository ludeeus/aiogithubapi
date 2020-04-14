"""
AIOGitHubAPI: Issue

https://developer.github.com/v3/issues/
"""
# pylint: disable=missing-docstring, unused-import
from aiogithubapi.objects.base import AIOGitHubAPIBase
from aiogithubapi.objects.repository.issue.comment import (
    AIOGitHubAPIRepositoryIssueComment,
    AIOGitHubAPIRepositoryIssueCommentUser,
)


class AIOGitHubAPIRepositoryIssue(AIOGitHubAPIBase):
    """Issue commment user GitHub API implementation."""

    def __init__(self, attributes):
        """Initialize."""
        self.attributes = attributes

    @property
    def html_url(self):
        return self.attributes.get("html_url")

    @property
    def id(self):
        return self.attributes.get("id")

    @property
    def number(self):
        return self.attributes.get("number")

    @property
    def labels(self):
        return self.attributes.get("labels", [])

    @property
    def title(self):
        return self.attributes.get("title")

    @property
    def state(self):
        return self.attributes.get("state")

    @property
    def assignees(self):
        return self.attributes.get("assignees")

    @property
    def body(self):
        return self.attributes.get("body")

    @property
    def user(self):
        return AIOGitHubAPIRepositoryIssueCommentUser(self.attributes.get("user"))
