"""
AioGitHub: Issue

https://developer.github.com/v3/issues/
"""
# pylint: disable=missing-docstring
from aiogithubapi.issuecomment import AIOGithubIssueCommentUser


class AIOGithubIssue:
    """Issue commment user Github API implementation."""

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
        return AIOGithubIssueCommentUser(self.attributes.get("user"))
