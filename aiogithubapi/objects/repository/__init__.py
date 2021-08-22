"""Deprecated"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from aiohttp.hdrs import IF_NONE_MATCH

# pylint: disable=redefined-builtin, missing-docstring, invalid-name, unused-import
from ...client import AIOGitHubAPIClient
from ...common.exceptions import AIOGitHubAPIException
from ...const import LOGGER
from ...objects.base import AIOGitHubAPIBaseClient
from ...objects.repos.commit import AIOGitHubAPIReposCommit
from ...objects.repository.content import (
    AIOGitHubAPIRepositoryContent,
    AIOGitHubAPIRepositoryTreeContent,
)
from ...objects.repository.issue import AIOGitHubAPIRepositoryIssue
from ...objects.repository.release import AIOGitHubAPIRepositoryRelease
from ...objects.repository.traffic import AIOGitHubAPIRepositoryTraffic
from ...objects.users.user import AIOGitHubAPIUsersUser


class AIOGitHubAPIRepository(AIOGitHubAPIBaseClient):
    """Repository GitHub API implementation."""

    def __init__(self, client: AIOGitHubAPIClient, attributes: dict) -> None:
        """Initialise."""
        super().__init__(client, attributes)
        self._last_commit = None
        self.traffic = AIOGitHubAPIRepositoryTraffic(client, attributes)

    @property
    def id(self) -> None:
        return self.attributes.get("id")

    @property
    def name(self) -> None:
        return self.attributes.get("name")

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
    def forks_count(self) -> int:
        return self.attributes.get("forks_count")

    @property
    def default_branch(self) -> None:
        return self.attributes.get("default_branch")

    @property
    def homepage(self) -> str:
        return self.attributes.get("homepage")

    @property
    def stargazers_count(self) -> str:
        return self.attributes.get("stargazers_count")

    @property
    def watchers_count(self) -> str:
        return self.attributes.get("watchers_count")

    @property
    def last_commit(self) -> None:
        if self._last_commit is None:
            LOGGER.warning("You need to call .set_last_commit to set this property")
        return self._last_commit

    @property
    def owner(self) -> AIOGitHubAPIUsersUser:
        return AIOGitHubAPIUsersUser(self.attributes.get("owner"))

    async def get_contents(
        self, path: str, ref: str or None = None, etag: Optional[str] = None
    ) -> list["AIOGitHubAPIRepositoryContent"] or "AIOGitHubAPIRepositoryContent":
        """Retrun a list of repository content objects."""
        _endpoint = f"/repos/{self.full_name}/contents/{path}"
        _params = {"path": path}
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag

        if ref is not None:
            _params["ref"] = ref.replace("tags/", "")

        response = await self.client.get(endpoint=_endpoint, params=_params, headers=_headers)
        if isinstance(response.data, list):
            return [AIOGitHubAPIRepositoryContent(x) for x in response.data]
        return AIOGitHubAPIRepositoryContent(response.data)

    async def get_tree(
        self, ref: str or None = None, etag: Optional[str] = None
    ) -> list["AIOGitHubAPIRepositoryTreeContent"] or list:
        """Retrun a list of repository tree objects."""
        if ref is None:
            raise AIOGitHubAPIException("Missing ref")
        _endpoint = f"/repos/{self.full_name}/git/trees/{ref}"
        _params = {"recursive": "1"}
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag

        response = await self.client.get(endpoint=_endpoint, params=_params, headers=_headers)

        return [
            AIOGitHubAPIRepositoryTreeContent(x, self.full_name, ref)
            for x in response.data.get("tree", [])
        ]

    async def get_rendered_contents(
        self, path: str, ref: str or None = None, etag: Optional[str] = None
    ) -> str:
        """Retrun a redered representation of a file."""
        _endpoint = f"/repos/{self.full_name}/contents/{path}"
        _headers = {"Accept": "application/vnd.github.v3.html"}
        _params = {"path": path}
        if etag:
            _headers[IF_NONE_MATCH] = etag

        if ref is not None:
            _params["ref"] = ref.replace("tags/", "")

        response = await self.client.get(
            endpoint=_endpoint, params=_params, headers=_headers, returnjson=False
        )
        return response.data

    async def get_releases(
        self, prerelease: bool = False, returnlimit: int = 5, etag: Optional[str] = None
    ) -> list["AIOGitHubAPIRepositoryRelease"] or list:
        """Retrun a list of repository release objects."""
        _endpoint = f"/repos/{self.full_name}/releases"
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag

        response = await self.client.get(endpoint=_endpoint, headers=_headers)
        contents = []

        for content in response.data or []:
            if len(contents) == returnlimit:
                break
            if not prerelease:
                if content.get("prerelease", False):
                    continue
            contents.append(AIOGitHubAPIRepositoryRelease(content))

        return contents

    async def set_last_commit(self, etag: Optional[str] = None) -> None:
        """Retrun a list of repository release objects."""
        _endpoint = f"/repos/{self.full_name}/branches/{self.default_branch}"
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag
        response = await self.client.get(endpoint=_endpoint, headers=_headers)
        self._last_commit = response.data["commit"]["sha"][0:7]

    async def get_last_commit(self, etag: Optional[str] = None) -> None:
        """Retrun a list of repository release objects."""
        _endpoint = f"/repos/{self.full_name}/branches/{self.default_branch}"
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag
        response = await self.client.get(endpoint=_endpoint, headers=_headers)
        return AIOGitHubAPIReposCommit(response.data.get("commit", {}))

    async def get_issue(
        self, issue: int, etag: Optional[str] = None
    ) -> "AIOGitHubAPIRepositoryIssue":
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues/{issue}"
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag

        response = await self.client.get(endpoint=_endpoint, headers=_headers)
        return AIOGitHubAPIRepositoryIssue(self.client, response.data)

    async def get_issues(self, etag: Optional[str] = None) -> list["AIOGitHubAPIRepositoryIssue"]:
        """Updates an issue comment."""
        _endpoint = f"/repos/{self.full_name}/issues"
        _headers = {}
        if etag:
            _headers[IF_NONE_MATCH] = etag

        response = await self.client.get(endpoint=_endpoint, headers=_headers)
        return [AIOGitHubAPIRepositoryIssue(self.client, x) for x in response.data or []]

    async def create_issue(
        self,
        title: str or None = None,
        body: str or None = None,
        state: str or None = None,
        milestone: int or None = None,
        labels: list[str] or None = None,
        assignees: list[str] or None = None,
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

        response = await self.client.post(endpoint=_endpoint, data=data, jsondata=True)
        return AIOGitHubAPIRepositoryIssue(self.client, response.data)
