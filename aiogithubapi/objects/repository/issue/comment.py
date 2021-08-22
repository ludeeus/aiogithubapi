"""
AIOGitHubAPI: Issue Comment

https://developer.github.com/v3/issues/comments/
"""
from ...base import AIOGitHubAPIBaseClient

# pylint: disable=missing-docstring
from ...content import AIOGitHubAPIContentBase
from ...users.user import AIOGitHubAPIUsersUser


class AIOGitHubAPIRepositoryIssueCommentUser(AIOGitHubAPIUsersUser):
    """Issue commment user GitHub API implementation."""

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


class AIOGitHubAPIRepositoryIssueComment(AIOGitHubAPIBaseClient):
    """Issue comment GitHub API implementation."""

    def __init__(self, client: AIOGitHubAPIContentBase, attributes: dict, repository: str):
        """Initialize."""
        super().__init__(client, attributes)
        self.repository = repository

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
        return AIOGitHubAPIRepositoryIssueCommentUser(self.attributes.get("user", {}))

    async def update(self, body: str) -> None:
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.repository}/issues/comments/{self.id}"

        await self.client.post(endpoint=_endpoint, data={"body": body}, jsondata=True)
