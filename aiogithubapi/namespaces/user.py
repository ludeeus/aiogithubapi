"""
Methods for the authenticated user namespace

https://docs.github.com/en/rest/reference/users#get-the-authenticated-user
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg
from ..models.repository import GitHubRepositoryModel
from ..models.response import GitHubResponseModel
from ..models.user import GitHubAuthenticatedUserModel
from .base import BaseNamespace


class GitHubUserNamespace(BaseNamespace):
    """Methods for the user namespace"""

    async def get(
        self,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubAuthenticatedUserModel]:
        """
         Get the authenticated user


        https://docs.github.com/en/rest/reference/users#get-a-user
        """
        response = await self._client.async_call_api(
            endpoint="/user",
            **kwargs,
        )
        response.data = GitHubAuthenticatedUserModel(response.data)

        return response

    async def starred(
        self,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubRepositoryModel]]:
        """
         Get the authenticated user starred repositories


        https://docs.github.com/en/rest/reference/users#get-a-user
        """
        response = await self._client.async_call_api(
            endpoint="/user/starred",
            **kwargs,
        )

        response.data = [GitHubRepositoryModel(data) for data in response.data]

        return response

    async def repos(
        self,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubRepositoryModel]]:
        """
         Get the repositories for the authenticated user


        https://docs.github.com/en/rest/reference/repos#list-repositories-for-a-user
        """
        response = await self._client.async_call_api(
            endpoint="/user/repos",
            **kwargs,
        )

        response.data = [GitHubRepositoryModel(data) for data in response.data]

        return response
