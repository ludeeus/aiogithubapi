"""
AIOGitHubAPI: Repository Content

https://developer.github.com/v3/repos/contents/
"""
# pylint: disable=missing-docstring
import base64

from ..content import AIOGitHubAPIContentBase


class AIOGitHubAPIRepositoryContent(AIOGitHubAPIContentBase):
    """Repository Conetent GitHub API implementation."""

    @property
    def type(self):
        return self.attributes.get("type", "file")

    @property
    def encoding(self):
        return self.attributes.get("encoding")

    @property
    def name(self):
        return self.attributes.get("name")

    @property
    def path(self):
        return self.attributes.get("path")

    @property
    def content(self):
        return base64.b64decode(bytearray(self.attributes.get("content"), "utf-8")).decode()

    @property
    def download_url(self):
        return self.attributes.get("download_url") or self.attributes.get("browser_download_url")


class AIOGitHubAPIRepositoryTreeContent(AIOGitHubAPIContentBase):
    """Repository Conetent GitHub API implementation."""

    def __init__(self, attributes, repository, ref):
        """Initialize."""
        self.attributes = attributes
        self.repository = repository
        self.ref = ref

    @property
    def full_path(self):
        return self.attributes.get("path")

    @property
    def is_directory(self):
        if self.attributes.get("type") == "tree":
            return True
        return False

    @property
    def path(self):
        path = ""
        if "/" in self.attributes.get("path"):
            path = self.attributes.get("path").split(
                f"/{self.attributes.get('path').split('/')[-1]}"
            )[0]
        return path

    @property
    def filename(self):
        filename = self.attributes.get("path")
        if "/" in self.attributes.get("path"):
            filename = self.attributes.get("path").split("/")[-1]
        return filename

    @property
    def url(self):
        return self.attributes.get("url")

    @property
    def download_url(self):
        return f"https://raw.githubusercontent.com/{self.repository}/{self.ref}/{self.attributes.get('path')}"
