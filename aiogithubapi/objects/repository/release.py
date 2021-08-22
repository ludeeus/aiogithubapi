"""
AIOGitHubAPI: Repository Release

https://developer.github.com/v3/repos/releases/
"""
# pylint: disable=missing-docstring
from datetime import datetime

from ...objects.base import AIOGitHubAPIBase
from ...objects.repository.content import AIOGitHubAPIRepositoryContent


class AIOGitHubAPIRepositoryRelease(AIOGitHubAPIBase):
    """Repository Release GitHub API implementation."""

    @property
    def tag_name(self):
        return self.attributes.get("tag_name")

    @property
    def name(self):
        return self.attributes.get("name")

    @property
    def published_at(self):
        return datetime.strptime(self.attributes.get("published_at"), "%Y-%m-%dT%H:%M:%SZ")

    @property
    def draft(self):
        return self.attributes.get("draft")

    @property
    def prerelease(self):
        return self.attributes.get("prerelease")

    @property
    def assets(self):
        return [AIOGitHubAPIRepositoryContent(x) for x in self.attributes.get("assets", [])]
