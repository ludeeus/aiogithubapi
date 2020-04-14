"""
AIOGitHubAPI: Issue Comment

https://developer.github.com/v3/issues/comments/
"""
# pylint: disable=missing-docstring
from aiogithubapi.objects.base import AIOGitHubAPIBase


class AIOGitHubAPIRepositoryIssueCommentUser(AIOGitHubAPIBase):
    """Issue commment user GitHub API implementation."""

    def __init__(self, attributes):
        """Initialize."""
        self.attributes = attributes

    @property
    def login(self):
        return self.attributes.get("login")

    @property
    def id(self):
        return self.attributes.get("id")

    @property
    def avatar_url(self):
        return self.attributes.get("avatar_url")

    @property
    def html_url(self):
        return self.attributes.get("html_url")

    @property
    def type(self):
        return self.attributes.get("type")

    @property
    def site_admin(self):
        return self.attributes.get("site_admin")


class AIOGitHubAPIRepositoryIssueComment(AIOGitHubAPIBase):
    """Issue comment GitHub API implementation."""

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
    def created_at(self):
        return self.attributes.get("created_at")

    @property
    def updated_at(self):
        return self.attributes.get("updated_at")

    @property
    def body(self):
        return self.attributes.get("body")

    @property
    def user(self):
        return AIOGitHubAPIRepositoryIssueCommentUser(self.attributes.get("user"))
