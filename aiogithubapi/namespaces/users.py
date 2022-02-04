"""
Methods for the users namespace

https://docs.github.com/en/rest/reference/users
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg
from ..models.repository import GitHubRepositoryModel
from ..models.response import GitHubResponseModel
from ..models.user import GitHubUserModel
from .base import BaseNamespace


class GitHubUsersNamespace(BaseNamespace):
    """Methods for the users namespace"""

    async def get(
        self,
        username: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubUserModel]:
        """
         Get a user

         **Arguments**:

         `username`

         The username to return, example "octocat"

        https://docs.github.com/en/rest/reference/users#get-a-user
        """
        response = await self._client.async_call_api(
            endpoint=f"/users/{username}",
            **kwargs,
        )
        response.data = GitHubUserModel(response.data)

        return response

    async def starred(
        self,
        username: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubRepositoryModel]]:
        """
         Get the starred repositories of a user

         **Arguments**:

         `username`

         The username to return, example "octocat"


        https://docs.github.com/en/rest/reference/users#get-a-user
        """
        response = await self._client.async_call_api(
            endpoint=f"/users/{username}/starred",
            **kwargs,
        )

        response.data = [GitHubRepositoryModel(data) for data in response.data]

        return response

    async def repos(
        self,
        username: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubRepositoryModel]]:
        """
         Get the repositories of a user

         **Arguments**:

         `username`

         The username to return, example "octocat"


        https://docs.github.com/en/rest/reference/repos#list-repositories-for-a-user
        """
        response = await self._client.async_call_api(
            endpoint=f"/users/{username}/repos",
            **kwargs,
        )

        response.data = [GitHubRepositoryModel(data) for data in response.data]

        return response
