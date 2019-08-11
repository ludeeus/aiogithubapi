"""
AioGitHub: Repository

https://developer.github.com/v3/repos/#get
"""
# pylint: disable=redefined-builtin, missing-docstring, invalid-name
from asyncio import CancelledError, TimeoutError, get_event_loop
from datetime import datetime

import async_timeout
from aiohttp import ClientError

import backoff

from aiogithubapi import (
    BASE_URL,
    GOOD_HTTP_CODES,
    AIOGitHub,
    AIOGithubRepositoryContent,
    AIOGithubRepositoryRelease,
    AIOGithubIssueComment,
    AIOGithubIssue,
    AIOGitHubException,
    AIOGitHubRatelimit,
)


class AIOGithubRepository(AIOGitHub):
    """Repository Github API implementation."""

    def __init__(self, attributes, token, session):
        """Initialize."""
        super().__init__(token, session)
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

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def get_contents(self, path, ref=None):
        """Retrun a list of repository content objects."""
        endpoint = "/repos/" + self.full_name + "/contents/" + path
        url = BASE_URL + endpoint

        params = {"path": path}
        if ref is not None:
            params["ref"] = ref.replace("tags/", "")

        await self.get_ratelimit()
        if self.ratelimits.remaining is not None and self.ratelimits.remaining == 0:
            raise AIOGitHubRatelimit("GitHub Ratelimit error")

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.get(url, headers=self.headers, params=params)
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")
            response = await response.json()

            if not isinstance(response, list):
                if response.get("message"):
                    if response.get("message") == "Not Found":
                        raise AIOGitHubException(
                            "{} does not exist in the repository.".format(path)
                        )
                    else:
                        raise AIOGitHubException(response["message"])
                return AIOGithubRepositoryContent(response)

            contents = []

            for content in response:
                contents.append(AIOGithubRepositoryContent(content))

        return contents

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def get_releases(self, prerelease=False):
        """Retrun a list of repository release objects."""
        endpoint = "/repos/{}/releases".format(self.full_name)
        url = BASE_URL + endpoint

        await self.get_ratelimit()
        if self.ratelimits.remaining is not None and self.ratelimits.remaining == 0:
            raise AIOGitHubRatelimit("GitHub Ratelimit error")

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.get(url, headers=self.headers)
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")
            response = await response.json()

            if not isinstance(response, list):
                if response.get("message"):
                    return False

            contents = []

            for content in response:
                if len(contents) == 5:
                    break
                if not prerelease:
                    if content.get("prerelease", False):
                        continue
                contents.append(AIOGithubRepositoryRelease(content))

        return contents

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def set_last_commit(self):
        """Retrun a list of repository release objects."""
        endpoint = "/repos/" + self.full_name + "/commits/" + self.default_branch
        url = BASE_URL + endpoint

        await self.get_ratelimit()
        if self.ratelimits.remaining is not None and self.ratelimits.remaining == 0:
            raise AIOGitHubRatelimit("GitHub Ratelimit error")

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.get(url, headers=self.headers)
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")

            response = await response.json()

            if response.get("message"):
                raise AIOGitHubException("No commits")

        self._last_commit = response["sha"][0:7]

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def get_issue(self, issue: int):
        """Updates an issue comment."""
        endpoint = f"/repos/{self.full_name}/issues/{issue}"
        url = BASE_URL + endpoint

        await self.get_ratelimit()
        if self.ratelimits.remaining is not None and self.ratelimits.remaining == 0:
            raise AIOGitHubRatelimit("GitHub Ratelimit error")

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.get(url, headers=self.headers)
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")

            response = await response.json()
            return AIOGithubIssue(response)

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def list_issue_comments(self, issue: int):
        """Updates an issue comment."""
        endpoint = f"/repos/{self.full_name}/issues/{issue}/comments"
        url = BASE_URL + endpoint

        await self.get_ratelimit()
        if self.ratelimits.remaining is not None and self.ratelimits.remaining == 0:
            raise AIOGitHubRatelimit("GitHub Ratelimit error")

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.get(url, headers=self.headers)
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")

            comments = []
            response = await response.json()
            for comment in response:
                comments.append(AIOGithubIssueComment(comment))
            return comments

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def comment_on_issue(self, issue: int, body: str):
        """Adds a comment to an issue."""
        endpoint = f"/repos/{self.full_name}/issues/{issue}/comments"
        url = BASE_URL + endpoint

        await self.get_ratelimit()
        if self.ratelimits.remaining is not None and self.ratelimits.remaining == 0:
            raise AIOGitHubRatelimit("GitHub Ratelimit error")

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.post(
                url, headers=self.headers, json={"body": body}
            )
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
    async def update_comment_on_issue(self, comment: int, body: str):
        """Updates an issue comment."""
        endpoint = f"/repos/{self.full_name}/issues/comments/{comment}"
        url = BASE_URL + endpoint

        await self.get_ratelimit()
        if self.ratelimits.remaining is not None and self.ratelimits.remaining == 0:
            raise AIOGitHubRatelimit("GitHub Ratelimit error")

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.patch(
                url, headers=self.headers, json={"body": body}
            )
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")

    @backoff.on_exception(
        backoff.expo, (ClientError, CancelledError, TimeoutError, KeyError), max_tries=5
    )
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
        endpoint = f"/repos/{self.full_name}/issues/{issue}"
        url = BASE_URL + endpoint

        await self.get_ratelimit()
        if self.ratelimits.remaining is not None and self.ratelimits.remaining == 0:
            raise AIOGitHubRatelimit("GitHub Ratelimit error")

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

        print(data)

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.session.patch(url, headers=self.headers, json=data)
            if response.status not in GOOD_HTTP_CODES:
                raise AIOGitHubException(f"GitHub returned {response.status} for {url}")

