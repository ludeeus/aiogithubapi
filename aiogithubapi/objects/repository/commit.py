"""
AIOGitHubAPI: Commit

https://docs.github.com/en/rest/reference/repos#get-a-commit
"""
# pylint: disable=missing-docstring
from aiogithubapi.objects.base import AIOGitHubAPIBase
from aiogithubapi.objects.user import AIOGitHubAPIUser


class _ParentObject(AIOGitHubAPIBase):
    @property
    def url(self):
        return self.attributes.get("url")

    @property
    def sha(self):
        return self.attributes.get("sha")


class _Tree(_ParentObject):
    pass


class _Parents(_ParentObject):
    pass


class _Actor(AIOGitHubAPIBase):
    @property
    def name(self):
        return self.attributes.get("name")

    @property
    def email(self):
        return self.attributes.get("email")

    @property
    def date(self):
        return self.attributes.get("date")


class _Verification(AIOGitHubAPIBase):
    @property
    def verified(self):
        return self.attributes.get("verified")

    @property
    def reason(self):
        return self.attributes.get("reason")

    @property
    def signature(self):
        return self.attributes.get("signature")

    @property
    def payload(self):
        return self.attributes.get("payload")


class _Commit(AIOGitHubAPIBase):
    @property
    def url(self):
        return self.attributes.get("url")

    @property
    def author(self):
        return _Actor(self.attributes.get("author", {}))

    @property
    def committer(self):
        return _Actor(self.attributes.get("committer", {}))

    @property
    def message(self):
        return self.attributes.get("message")

    @property
    def message_short(self):
        return self.attributes.get("message", "").split("\n")[0]

    @property
    def tree(self):
        return _Tree(self.attributes.get("tree", []))

    @property
    def comment_count(self):
        return self.attributes.get("comment_count")

    @property
    def verification(self):
        return _Verification(self.attributes.get("verification", {}))


class _Stats(AIOGitHubAPIBase):
    @property
    def additions(self):
        return self.attributes.get("additions")

    @property
    def deletions(self):
        return self.attributes.get("deletions")

    @property
    def total(self):
        return self.attributes.get("total")


class _Files(AIOGitHubAPIBase):
    @property
    def filename(self):
        return self.attributes.get("filename")

    @property
    def additions(self):
        return self.attributes.get("additions")

    @property
    def deletions(self):
        return self.attributes.get("deletions")

    @property
    def changes(self):
        return self.attributes.get("changes")

    @property
    def status(self):
        return self.attributes.get("status")

    @property
    def raw_url(self):
        return self.attributes.get("raw_url")

    @property
    def blob_url(self):
        return self.attributes.get("blob_url")

    @property
    def patch(self):
        return self.attributes.get("patch")


class AIOGitHubAPIRepositoryCommit(AIOGitHubAPIBase):
    """Commit GitHub API implementation."""

    @property
    def url(self):
        return self.attributes.get("url")

    @property
    def sha(self):
        return self.attributes.get("sha")

    @property
    def sha_short(self):
        return self.attributes.get("sha")[0:7]

    @property
    def node_id(self):
        return self.attributes.get("node_id")

    @property
    def html_url(self):
        return self.attributes.get("html_url")

    @property
    def comments_url(self):
        return self.attributes.get("comments_url")

    @property
    def commit(self):
        return _Commit(self.attributes.get("commit", {}))

    @property
    def author(self):
        return AIOGitHubAPIUser(self.attributes.get("author", {}))

    @property
    def committer(self):
        return AIOGitHubAPIUser(self.attributes.get("committer", {}))

    @property
    def parents(self):
        return [_Parents(x) for x in self.attributes.get("parents", [])]

    @property
    def stats(self):
        return _Stats(self.attributes.get("stats", {}))

    @property
    def files(self):
        return [_Files(x) for x in self.attributes.get("files", [])]
