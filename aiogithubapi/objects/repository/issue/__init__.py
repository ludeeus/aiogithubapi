"""
AIOGitHubAPI: Issue

https://developer.github.com/v3/issues/
"""
# pylint: disable=missing-docstring, unused-import
from ...base import AIOGitHubAPIBaseClient
from ...repository.issue.comment import (
    AIOGitHubAPIRepositoryIssueComment,
    AIOGitHubAPIRepositoryIssueCommentUser,
)


class AIOGitHubAPIRepositoryIssue(AIOGitHubAPIBaseClient):
    """Issue commment user GitHub API implementation."""

    @property
    def html_url(self):
        return self.attributes.get("html_url")

    @property
    def id(self):
        return self.attributes.get("id")

    @property
    def number(self):
        return self.attributes.get("number")

    @property
    def labels(self):
        return self.attributes.get("labels", [])

    @property
    def title(self):
        return self.attributes.get("title")

    @property
    def state(self):
        return self.attributes.get("state")

    @property
    def assignees(self):
        return self.attributes.get("assignees")

    @property
    def body(self):
        return self.attributes.get("body")

    @property
    def repository(self):
        repository_url = self.attributes.get("repository_url").split("/")
        return f"{repository_url[-2]}/{repository_url[-1]}"

    @property
    def user(self):
        return AIOGitHubAPIRepositoryIssueCommentUser(self.attributes.get("user"))

    async def get_comments(
        self,
    ) -> ["AIOGitHubAPIRepositoryIssueComment"] or list:
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.repository}/issues/{self.id}/comments"

        response = await self.client.get(endpoint=_endpoint)

        return [
            AIOGitHubAPIRepositoryIssueComment(self.client, x, self.repository)
            for x in response.data or []
        ]

    async def comment(self, body: str) -> None:
        """Adds a comment to an issue."""
        _endpoint = f"/repos/{self.repository}/issues/{self.id}/comments"

        await self.client.post(endpoint=_endpoint, data={"body": body}, jsondata=True)

    async def update(
        self,
        title: str or None = None,
        body: str or None = None,
        state: str or None = None,
        milestone: int or None = None,
        labels: [str] or None = None,
        assignees: [str] or None = None,
    ):
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.repository}/issues/{self.id}"

        data = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if state is not None:
            data["state"] = state
        if milestone is not None:
            data["milestone"] = milestone
        if labels is not None:
            data["labels"] = labels
        if assignees is not None:
            data["assignees"] = assignees

        await self.client.post(endpoint=_endpoint, data=data, jsondata=True)
