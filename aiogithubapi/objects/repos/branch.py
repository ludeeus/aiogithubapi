"""
Class object for AIOGitHubAPIReposBranch
Documentation: https://docs.github.com/en/rest/reference/repos#get-a-branch

Generated by generate/generate.py - 2020-08-02 10:29:03.550853
"""

from ..base import AIOGitHubAPIBase


class CommitCommitAuthor(AIOGitHubAPIBase):
    @property
    def name(self):
        return self.attributes.get("name", "")

    @property
    def date(self):
        return self.attributes.get("date", "")

    @property
    def email(self):
        return self.attributes.get("email", "")


class CommitCommitTree(AIOGitHubAPIBase):
    @property
    def sha(self):
        return self.attributes.get("sha", "")

    @property
    def url(self):
        return self.attributes.get("url", "")


class CommitCommitCommitter(AIOGitHubAPIBase):
    @property
    def name(self):
        return self.attributes.get("name", "")

    @property
    def date(self):
        return self.attributes.get("date", "")

    @property
    def email(self):
        return self.attributes.get("email", "")


class CommitCommitVerification(AIOGitHubAPIBase):
    @property
    def verified(self):
        return self.attributes.get("verified", False)

    @property
    def reason(self):
        return self.attributes.get("reason", "")

    @property
    def signature(self):
        return self.attributes.get("signature", None)

    @property
    def payload(self):
        return self.attributes.get("payload", None)


class CommitCommit(AIOGitHubAPIBase):
    @property
    def author(self):
        return CommitCommitAuthor(self.attributes.get("author", {}))

    @property
    def url(self):
        return self.attributes.get("url", "")

    @property
    def message(self):
        return self.attributes.get("message", "")

    @property
    def tree(self):
        return CommitCommitTree(self.attributes.get("tree", {}))

    @property
    def committer(self):
        return CommitCommitCommitter(self.attributes.get("committer", {}))

    @property
    def verification(self):
        return CommitCommitVerification(self.attributes.get("verification", {}))


class CommitAuthor(AIOGitHubAPIBase):
    @property
    def gravatar_id(self):
        return self.attributes.get("gravatar_id", "")

    @property
    def avatar_url(self):
        return self.attributes.get("avatar_url", "")

    @property
    def url(self):
        return self.attributes.get("url", "")

    @property
    def id(self):
        return self.attributes.get("id", None)

    @property
    def login(self):
        return self.attributes.get("login", "")


class Parents(AIOGitHubAPIBase):
    @property
    def sha(self):
        return self.attributes.get("sha", "")

    @property
    def url(self):
        return self.attributes.get("url", "")


class CommitCommitter(AIOGitHubAPIBase):
    @property
    def gravatar_id(self):
        return self.attributes.get("gravatar_id", "")

    @property
    def avatar_url(self):
        return self.attributes.get("avatar_url", "")

    @property
    def url(self):
        return self.attributes.get("url", "")

    @property
    def id(self):
        return self.attributes.get("id", None)

    @property
    def login(self):
        return self.attributes.get("login", "")


class Commit(AIOGitHubAPIBase):
    @property
    def sha(self):
        return self.attributes.get("sha", "")

    @property
    def node_id(self):
        return self.attributes.get("node_id", "")

    @property
    def commit(self):
        return CommitCommit(self.attributes.get("commit", {}))

    @property
    def author(self):
        return CommitAuthor(self.attributes.get("author", {}))

    @property
    def parents(self):
        return [Parents(x) for x in self.attributes.get("parents", [])]

    @property
    def url(self):
        return self.attributes.get("url", "")

    @property
    def committer(self):
        return CommitCommitter(self.attributes.get("committer", {}))


class ProtectionRequiredStatusChecks(AIOGitHubAPIBase):
    @property
    def enforcement_level(self):
        return self.attributes.get("enforcement_level", "")

    @property
    def contexts(self):
        return self.attributes.get("contexts", [])


class Protection(AIOGitHubAPIBase):
    @property
    def enabled(self):
        return self.attributes.get("enabled", True)

    @property
    def required_status_checks(self):
        return ProtectionRequiredStatusChecks(self.attributes.get("required_status_checks", {}))


class AIOGitHubAPIReposBranch(AIOGitHubAPIBase):
    @property
    def name(self):
        return self.attributes.get("name", "")

    @property
    def commit(self):
        return Commit(self.attributes.get("commit", {}))

    @property
    def protected(self):
        return self.attributes.get("protected", True)

    @property
    def protection(self):
        return Protection(self.attributes.get("protection", {}))

    @property
    def protection_url(self):
        return self.attributes.get("protection_url", "")
