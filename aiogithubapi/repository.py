"""
AioGitHub: Repository

https://developer.github.com/v3/repos/#get
"""
# pylint: disable=redefined-builtin, missing-docstring, invalid-name
from datetime import datetime

from aiogithubapi import (
    AIOGithubRepositoryContent,
    AIOGithubTreeContent,
    AIOGithubRepositoryRelease,
    AIOGithubIssueComment,
    AIOGithubIssue,
    AIOGitHubException,
)


class AIOGithubRepository:
    """Repository Github API implementation."""

    def __init__(self, client, attributes):
        """Initialize."""
        self.client = client
        self.attributes = attributes
        self._last_commit = None

    @property
    def id(self):
        return self.attributes.get("id")

    @property
    def full_name(self):
        return self.attributes.get("full_name")

    @property
    def pushed_at(self):
        return datetime.strptime(self.attributes.get("pushed_at"), "%Y-%m-%dT%H:%M:%SZ")

    @property
    def archived(self):
        return self.attributes.get("archived")

    @property
    def description(self):
        return self.attributes.get("description")

    @property
    def topics(self):
        return self.attributes.get("topics")

    @property
    def fork(self):
        return self.attributes.get("fork")

    @property
    def default_branch(self):
        return self.attributes.get("default_branch")

    @property
    def last_commit(self):
        return self._last_commit

    async def get_contents(self, path, ref=None):
        """Retrun a list of repository content objects."""
        _endpoint = f"/repos/{self.full_name}/contents/{path}"
        _params = {"path": path}

        if ref is not None:
            _params["ref"] = ref.replace("tags/", "")

        response = await self.client.get(endpoint=_endpoint, params=_params)
        return [AIOGithubRepositoryContent(x) for x in response or []]

    async def get_tree(self, ref=None):
        """Retrun a list of repository tree objects."""
        if ref is None:
            raise AIOGitHubException("Missing ref")
        _endpoint = f"/repos/{self.full_name}/git/trees/{ref}"
        _params = {"recursive": "1"}

        response = await self.client.get(endpoint=_endpoint, params=_params)

        return [
            AIOGithubTreeContent(x, self.full_name, ref)
            for x in response.get("tree", [])
        ]

    async def get_rendered_contents(self, path, ref=None):
        """Retrun a redered representation of a file."""
        _endpoint = f"/repos/{self.full_name}/contents/{path}"
        _headers = {"Accept": "application/vnd.github.v3.html"}
        _params = {"path": path}

        if ref is not None:
            _params["ref"] = ref.replace("tags/", "")

        return await self.client.get(
            endpoint=_endpoint, params=_params, headers=_headers, returnjson=False
        )

    async def get_releases(self, prerelease=False, returnlimit=5):
        """Retrun a list of repository release objects."""
        _endpoint = f"/repos/{self.full_name}/releases"

        response = await self.client.get(endpoint=_endpoint)
        contents = []

        for content in response or []:
            if len(contents) == returnlimit:
                break
            if not prerelease:
                if content.get("prerelease", False):
                    continue
            contents.append(AIOGithubRepositoryRelease(content))

        return contents

    async def set_last_commit(self):
        """Retrun a list of repository release objects."""
        _endpoint = f"/repos/{self.full_name}/commits/{self.default_branch}"

        response = await self.client.get(endpoint=_endpoint)
        self._last_commit = response["sha"][0:7]

    async def get_issue(self, issue: int):
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues/{issue}"

        response = await self.client.get(endpoint=_endpoint)
        return AIOGithubIssue(response)

    async def list_issue_comments(self, issue: int):
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues/{issue}/comments"

        response = await self.client.get(endpoint=_endpoint)

        return [AIOGithubIssueComment(x) for x in response or []]

    async def comment_on_issue(self, issue: int, body: str):
        """Adds a comment to an issue."""
        _endpoint = f"/repos/{self.full_name}/issues/{issue}/comments"

        await self.client.post(endpoint=_endpoint, data={"body": body}, jsondata=True)

    async def update_comment_on_issue(self, comment: int, body: str):
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues/comments/{comment}"

        await self.client.post(endpoint=_endpoint, data={"body": body}, jsondata=True)

    async def update_issue(
        self,
        issue: int,
        title=None,
        body=None,
        state=None,
        milestone=None,
        labels=None,
        assignees=None,
    ):
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues/{issue}"

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
