"""
AIOGitHubAPI: Commit

https://docs.github.com/en/rest/reference/repos#get-a-commit
"""
# pylint: disable=missing-docstring
from aiogithubapi.objects.base import AIOGitHubAPIBase


class AIOGitHubAPIUser(AIOGitHubAPIBase):
    """User GitHub API implementation."""

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
    def node_id(self):
        return self.attributes.get("node_id")

    @property
    def avatar_url(self):
        return self.attributes.get("avatar_url")

    @property
    def gravatar_id(self):
        return self.attributes.get("gravatar_id")

    @property
    def url(self):
        return self.attributes.get("url")

    @property
    def html_url(self):
        return self.attributes.get("html_url")

    @property
    def followers_url(self):
        return self.attributes.get("followers_url")

    @property
    def following_url(self):
        return self.attributes.get("following_url")

    @property
    def gists_url(self):
        return self.attributes.get("gists_url")

    @property
    def starred_url(self):
        return self.attributes.get("starred_url")

    @property
    def subscriptions_url(self):
        return self.attributes.get("subscriptions_url")

    @property
    def organizations_url(self):
        return self.attributes.get("organizations_url")

    @property
    def repos_url(self):
        return self.attributes.get("repos_url")

    @property
    def events_url(self):
        return self.attributes.get("events_url")

    @property
    def received_events_url(self):
        return self.attributes.get("received_events_url")

    @property
    def type(self):
        return self.attributes.get("type")

    @property
    def site_admin(self):
        return self.attributes.get("site_admin", False)
