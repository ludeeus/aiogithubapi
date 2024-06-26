"""
Class object for AIOGitHubAPIReposTrafficClones
Documentation: https://docs.github.com/en/rest/reference/repos#get-repository-clones

Generated by generate/generate.py - 2020-08-02 12:24:23.865974
"""

from ...base import AIOGitHubAPIBase


class Clones(AIOGitHubAPIBase):
    @property
    def timestamp(self):
        return self.attributes.get("timestamp", "")

    @property
    def count(self):
        return self.attributes.get("count", None)

    @property
    def uniques(self):
        return self.attributes.get("uniques", None)


class AIOGitHubAPIReposTrafficClones(AIOGitHubAPIBase):
    @property
    def count(self):
        return self.attributes.get("count", None)

    @property
    def uniques(self):
        return self.attributes.get("uniques", None)

    @property
    def clones(self):
        return [Clones(x) for x in self.attributes.get("clones", [])]
