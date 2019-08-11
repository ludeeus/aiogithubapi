"""
AioGitHub: Issue Comment

https://developer.github.com/v3/issues/comments/
"""
# pylint: disable=missing-docstring


class AIOGithubIssueCommentUser:
    """Issue commment user Github API implementation."""

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


class AIOGithubIssueComment:
    """Issue comment Github API implementation."""

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
        return AIOGithubIssueCommentUser(self.attributes.get("user"))
