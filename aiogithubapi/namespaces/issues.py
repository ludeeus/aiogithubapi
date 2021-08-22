"""
Methods for the issues namespace

https://docs.github.com/en/rest/reference/issues
"""
from __future__ import annotations

from typing import Any, Dict, List

from ..const import (
    GitHubIssueLockReason,
    GitHubRequestKwarg,
    HttpMethod,
    RepositoryType,
)
from ..helpers import repository_full_name
from ..models.issue import GitHubIssueModel
from ..models.issue_comment import GitHubIssueCommentModel
from ..models.response import GitHubResponseModel
from .base import BaseNamespace


class GitHubIssuesNamespace(BaseNamespace):
    """
    Methods for the issues namespace

    Note: GitHub's REST API v3 considers every pull request an issue,
    but not every issue is a pull request. For this reason, "Issues"
    endpoints may return both issues and pull requests in the response.
    You can identify pull requests by the pull_request key.
    """

    async def get(
        self,
        repository: RepositoryType,
        issue_number: int | str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubIssueModel]:
        """
         Get an issue

         **Arguments**:

         `repository`

         The repository the issue belong to, example "octocat/hello-world"

         `issue_number`

         The issue number to return, example "1"

        https://docs.github.com/en/rest/reference/issues#get-an-issue
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/issues/{issue_number}",
            **kwargs,
        )
        response.data = GitHubIssueModel(response.data)
        return response

    async def create(
        self,
        repository: RepositoryType,
        data: Dict[str, Any],
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubIssueModel]:
        """
         Create an issue

         **Arguments**:

         `repository`

         The repository the issue belong to, example "octocat/hello-world"

         `data`

         The data the issue will be created with, example {"title": "new title"}

        https://docs.github.com/en/rest/reference/issues#create-an-issue
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/issues",
            data=data,
            **{**kwargs, GitHubRequestKwarg.METHOD: HttpMethod.POST},
        )
        response.data = GitHubIssueModel(response.data)
        return response

    async def update(
        self,
        repository: RepositoryType,
        issue_number: int | str,
        data: Dict[str, Any],
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubIssueModel]:
        """
         Update an issue

         **Arguments**:

         `repository`

         The repository the issue belong to, example "octocat/hello-world"

         `issue_number`

         The issue number to update, example "1"

         `data`

         The data to update, example {"title": "new title"}

        https://docs.github.com/en/rest/reference/issues#update-an-issue
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/issues/{issue_number}",
            data=data,
            **{**kwargs, GitHubRequestKwarg.METHOD: HttpMethod.PATCH},
        )
        response.data = GitHubIssueModel(response.data)
        return response

    async def lock(
        self,
        repository: RepositoryType,
        issue_number: int | str,
        lock_reason: GitHubIssueLockReason,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[None]:
        """
         Lock an issue

         **Arguments**:

         `repository`

         The repository the comment belong to, example "octocat/hello-world"

         `issue_number`

         The issue number to lock, example "1"

         `lock_reason`

         The reason why the issue was locked;
            * off-topic
            * too heated
            * resolved
            * spam

        https://docs.github.com/en/rest/reference/issues#lock-an-issue
        """
        response = await self._client.async_call_api(
            endpoint=(f"/repos/{repository_full_name(repository)}/issues/{issue_number}/lock"),
            data={"lock_reason": lock_reason},
            **{**kwargs, GitHubRequestKwarg.METHOD: HttpMethod.PUT},
        )
        return response

    async def unlock(
        self,
        repository: RepositoryType,
        issue_number: int | str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[None]:
        """
         Unlock an issue

         **Arguments**:

         `repository`

         The repository the comment belong to, example "octocat/hello-world"

         `issue_number`

         The issue number to lock, example "1"

        https://docs.github.com/en/rest/reference/issues#unlock-an-issue
        """
        response = await self._client.async_call_api(
            endpoint=(f"/repos/{repository_full_name(repository)}/issues/{issue_number}/lock"),
            **{**kwargs, GitHubRequestKwarg.METHOD: HttpMethod.DELETE},
        )
        return response

    async def list(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[List[GitHubIssueModel]]:
        """
         List repository issues

         **Arguments**:

         `repository`

         The repository to return, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/issues#list-repository-issues
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/issues",
            **kwargs,
        )
        response.data = [GitHubIssueModel(data) for data in response.data]
        return response

    async def get_comment(
        self,
        repository: RepositoryType,
        comment_id: int | str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[List[GitHubIssueCommentModel]]:
        """
         Get an issue comment

         **Arguments**:

         `repository`

         The repository the issue belong to, example "octocat/hello-world"

         `comment_id`

         The ID of a comment in an issue number to return, example "1"

        https://docs.github.com/en/rest/reference/issues#list-issue-comments
        """
        response = await self._client.async_call_api(
            endpoint=(
                f"/repos/{repository_full_name(repository)}" f"/issues/comments/{comment_id}"
            ),
            **kwargs,
        )
        response.data = GitHubIssueCommentModel(response.data)
        return response

    async def create_comment(
        self,
        repository: RepositoryType,
        issue_number: int | str,
        data: Dict[str, Any],
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubIssueCommentModel]:
        """
         Create an issue comment

         **Arguments**:

         `repository`

         The repository the issue belong to, example "octocat/hello-world"

         `issue_number`

         The issue number to create a comment in, example "1"

         `data`

         The data the issue will be created with, example {"body": "test"}

        https://docs.github.com/en/rest/reference/issues#create-an-issue-comment
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/issues/{issue_number}/comments",
            data=data,
            **{**kwargs, GitHubRequestKwarg.METHOD: HttpMethod.POST},
        )
        response.data = GitHubIssueCommentModel(response.data)
        return response

    async def update_comment(
        self,
        repository: RepositoryType,
        comment_id: int | str,
        data: Dict[str, Any],
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubIssueCommentModel]:
        """
         Update an issue comment

         **Arguments**:

         `repository`

         The repository the comment belong to, example "octocat/hello-world"

         `comment_id`

         The ID of a comment in an issue number to update, example "1"

         `data`

         The data the issue will be created with, example {"body": "test"}

        https://docs.github.com/en/rest/reference/issues#update-an-issue-comment
        """
        response = await self._client.async_call_api(
            endpoint=(
                f"/repos/{repository_full_name(repository)}" f"/issues/comments/{comment_id}"
            ),
            data=data,
            **{**kwargs, GitHubRequestKwarg.METHOD: HttpMethod.PATCH},
        )
        response.data = GitHubIssueCommentModel(response.data)
        return response

    async def delete_comment(
        self,
        repository: RepositoryType,
        comment_id: int | str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[None]:
        """
         Delete an issue comment

         **Arguments**:

         `repository`

         The repository the comment belong to, example "octocat/hello-world"

         `comment_id`

         The ID of a comment in an issue number to delete, example "1"

        https://docs.github.com/en/rest/reference/issues#delete-an-issue-comment
        """
        response = await self._client.async_call_api(
            endpoint=(
                f"/repos/{repository_full_name(repository)}" f"/issues/comments/{comment_id}"
            ),
            **{**kwargs, GitHubRequestKwarg.METHOD: HttpMethod.DELETE},
        )
        return response

    async def list_comments(
        self,
        repository: RepositoryType,
        issue_number: int | str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[List[GitHubIssueCommentModel]]:
        """
         List issue comments

         **Arguments**:

         `repository`

         The repository the comments belong to, example "octocat/hello-world"

         `issue_number`

         The issue number to return comments for, example "1"

        https://docs.github.com/en/rest/reference/issues#list-issue-comments
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/issues/{issue_number}/comments",
            **kwargs,
        )
        response.data = [GitHubIssueCommentModel(data) for data in response.data]
        return response
