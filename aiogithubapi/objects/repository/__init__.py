"""
AIOGitHubAPI: Repository

https://developer.github.com/v3/repos/#get
"""
# pylint: disable=redefined-builtin, missing-docstring, invalid-name, unused-import
from datetime import datetime

from aiogithubapi.common.exceptions import AIOGitHubAPIException
from aiogithubapi.objects.base import AIOGitHubAPIBase

from aiogithubapi.objects.repository.content import (
    AIOGitHubAPIRepositoryContent,
    AIOGitHubAPIRepositoryTreeContent,
)
from aiogithubapi.objects.repository.issue import (
    AIOGitHubAPIRepositoryIssue,
    AIOGitHubAPIRepositoryIssueComment,
    AIOGitHubAPIRepositoryIssueCommentUser,
)
from aiogithubapi.objects.repository.release import AIOGitHubAPIRepositoryRelease


class AIOGitHubAPIRepository(AIOGitHubAPIBase):
    """Repository GitHub API implementation."""

    def __init__(self, client: "AIOGitHubAPIClient", attributes: dict) -> None:
        """Initialise."""
        self.client = client
        self.attributes = attributes
        self._last_commit = None

    @property
    def id(self) -> None:
        return self.attributes.get("id")

    @property
    def full_name(self) -> None:
        return self.attributes.get("full_name")

    @property
    def pushed_at(self) -> None:
        return datetime.strptime(self.attributes.get("pushed_at"), "%Y-%m-%dT%H:%M:%SZ")

    @property
    def archived(self) -> None:
        return self.attributes.get("archived")

    @property
    def description(self) -> None:
        return self.attributes.get("description")

    @property
    def topics(self) -> None:
        return self.attributes.get("topics")

    @property
    def fork(self) -> None:
        return self.attributes.get("fork")

    @property
    def default_branch(self) -> None:
        return self.attributes.get("default_branch")

    @property
    def last_commit(self) -> None:
        return self._last_commit

    async def get_contents(
        self, path: str, ref: str or None = None
    ) -> ["AIOGitHubAPIRepositoryContent"] or "AIOGitHubAPIRepositoryContent":
        """Retrun a list of repository content objects."""
        _endpoint = f"/repos/{self.full_name}/contents/{path}"
        _params = {"path": path}

        if ref is not None:
            _params["ref"] = ref.replace("tags/", "")

        response = await self.client.get(endpoint=_endpoint, params=_params)
        if isinstance(response, list):
            return [AIOGitHubAPIRepositoryContent(x) for x in response]
        return AIOGitHubAPIRepositoryContent(response)

    async def get_tree(
        self, ref: str or None = None
    ) -> ["AIOGitHubAPIRepositoryTreeContent"] or list:
        """Retrun a list of repository tree objects."""
        if ref is None:
            raise AIOGitHubAPIException("Missing ref")
        _endpoint = f"/repos/{self.full_name}/git/trees/{ref}"
        _params = {"recursive": "1"}

        response = await self.client.get(endpoint=_endpoint, params=_params)

        return [
            AIOGitHubAPIRepositoryTreeContent(x, self.full_name, ref)
            for x in response.get("tree", [])
        ]

    async def get_rendered_contents(self, path: str, ref: str or None = None) -> str:
        """Retrun a redered representation of a file."""
        _endpoint = f"/repos/{self.full_name}/contents/{path}"
        _headers = {"Accept": "application/vnd.github.v3.html"}
        _params = {"path": path}

        if ref is not None:
            _params["ref"] = ref.replace("tags/", "")

        return await self.client.get(
            endpoint=_endpoint, params=_params, headers=_headers, returnjson=False
        )

    async def get_releases(
        self, prerelease: bool = False, returnlimit: int = 5
    ) -> ["AIOGitHubAPIRepositoryRelease"] or list:
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
            contents.append(AIOGitHubAPIRepositoryRelease(content))

        return contents

    async def set_last_commit(self) -> None:
        """Retrun a list of repository release objects."""
        _endpoint = f"/repos/{self.full_name}/branches/{self.default_branch}"
        response = await self.client.get(endpoint=_endpoint)
        self._last_commit = response["commit"]["sha"][0:7]

    async def get_issue(self, issue: int) -> "AIOGitHubAPIRepositoryIssue":
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues/{issue}"

        response = await self.client.get(endpoint=_endpoint)
        return AIOGitHubAPIRepositoryIssue(self.client, response)

    async def get_issues(self) -> ["AIOGitHubAPIRepositoryIssue"]:
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues"

        response = await self.client.get(endpoint=_endpoint)
        return [AIOGitHubAPIRepositoryIssue(self.client, x) for x in response or []]

    async def create_issue(
        self,
        title: str or None = None,
        body: str or None = None,
        state: str or None = None,
        milestone: int or None = None,
        labels: [str] or None = None,
        assignees: [str] or None = None,
    ):
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues"

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

        issue = await self.client.post(endpoint=_endpoint, data=data, jsondata=True)
        return AIOGitHubAPIRepositoryIssue(self.client, issue)
