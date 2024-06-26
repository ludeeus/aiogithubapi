"""
Class object for AIOGitHubAPIReposLabel
Documentation: https://docs.github.com/en/rest/reference/issues#get-a-label

Generated by generate/generate.py - 2020-08-02 10:32:07.005845
"""

from ..base import AIOGitHubAPIBase


class AIOGitHubAPIReposLabel(AIOGitHubAPIBase):
    @property
    def id(self):
        return self.attributes.get("id", None)

    @property
    def node_id(self):
        return self.attributes.get("node_id", "")

    @property
    def url(self):
        return self.attributes.get("url", "")

    @property
    def name(self):
        return self.attributes.get("name", "")

    @property
    def description(self):
        return self.attributes.get("description", "")

    @property
    def color(self):
        return self.attributes.get("color", "")

    @property
    def default(self):
        return self.attributes.get("default", True)
