
"""
Class object for AIOGitHubAPIRepositoryBranch
Documentation: https://docs.github.com/en/rest/reference/repos#get-a-branch
API Path: /repos/{owner}/{repo}/branches/{branch}
"""
from aiogithubapi.objects.base import AIOGitHubAPIBase


class _Author(AIOGitHubAPIBase):

    @property
    def name(self):
        return self.attributes.get("name", "")

    @property
    def date(self):
        return self.attributes.get("date", "")

    @property
    def email(self):
        return self.attributes.get("email", "")


class _Tree(AIOGitHubAPIBase):

    @property
    def sha(self):
        return self.attributes.get("sha", "")

    @property
    def url(self):
        return self.attributes.get("url", "")


class _Committer(AIOGitHubAPIBase):

    @property
    def name(self):
        return self.attributes.get("name", "")

    @property
    def date(self):
        return self.attributes.get("date", "")

    @property
    def email(self):
        return self.attributes.get("email", "")


class _Verification(AIOGitHubAPIBase):

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


class _Commit(AIOGitHubAPIBase):

    @property
    def author(self):
        return _Author(self.attributes.get("author", {}))

    @property
    def url(self):
        return self.attributes.get("url", "")

    @property
    def message(self):
        return self.attributes.get("message", "")

    @property
    def tree(self):
        return _Tree(self.attributes.get("tree", {}))

    @property
    def committer(self):
        return _Committer(self.attributes.get("committer", {}))

    @property
    def verification(self):
        return _Verification(self.attributes.get("verification", {}))


class _Author(AIOGitHubAPIBase):

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


class _Committer(AIOGitHubAPIBase):

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


class _Commit(AIOGitHubAPIBase):

    @property
    def sha(self):
        return self.attributes.get("sha", "")

    @property
    def node_id(self):
        return self.attributes.get("node_id", "")

    @property
    def commit(self):
        return _Commit(self.attributes.get("commit", {}))

    @property
    def author(self):
        return _Author(self.attributes.get("author", {}))

    @property
    def url(self):
        return self.attributes.get("url", "")

    @property
    def committer(self):
        return _Committer(self.attributes.get("committer", {}))


class _RequiredStatusChecks(AIOGitHubAPIBase):

    @property
    def enforcement_level(self):
        return self.attributes.get("enforcement_level", "")


class _Protection(AIOGitHubAPIBase):

    @property
    def enabled(self):
        return self.attributes.get("enabled", True)

    @property
    def required_status_checks(self):
        return _RequiredStatusChecks(self.attributes.get("required_status_checks", {}))


class RepositoryBranch(AIOGitHubAPIBase):

    @property
    def name(self):
        return self.attributes.get("name", "")

    @property
    def commit(self):
        return _Commit(self.attributes.get("commit", {}))

    @property
    def protected(self):
        return self.attributes.get("protected", True)

    @property
    def protection(self):
        return _Protection(self.attributes.get("protection", {}))

    @property
    def protection_url(self):
        return self.attributes.get("protection_url", "")



