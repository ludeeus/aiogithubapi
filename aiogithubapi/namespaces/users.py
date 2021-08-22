"""
Methods for the users namespace

https://docs.github.com/en/rest/reference/users
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg
from ..models.response import GitHubResponseModel
from ..models.user import GitHubAuthenticatedUserModel, GitHubUserModel
from .base import BaseNamespace


class GitHubUsersNamespace(BaseNamespace):
    """Methods for the users namespace"""

    async def get(
        self,
        username: str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubAuthenticatedUserModel | GitHubUserModel]:
        """
         Get a user

         **Arguments**:

         `username` (Optional)

         The username to return, example "octocat", if not provided,
         the authenticated user is returned

        https://docs.github.com/en/rest/reference/users#get-a-user
        """
        response = await self._client.async_call_api(
            endpoint="/user" if not username else f"/users/{username}",
            **kwargs,
        )
        if username:
            response.data = GitHubUserModel(response.data)
        else:
            response.data = GitHubAuthenticatedUserModel(response.data)

        return response
