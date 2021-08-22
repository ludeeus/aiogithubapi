"""
Methods for the issues namespace

https://docs.github.com/en/rest/reference/pulls
"""
from typing import Any, Dict, List

from ..const import GitHubRequestKwarg, RepositoryType
from ..helpers import repository_full_name
from ..models.pull_request import GitHubPullRequestModel
from ..models.response import GitHubResponseModel
from .base import BaseNamespace


class GitHubPullsNamespace(BaseNamespace):
    """
    Methods for the pull requests namespace

    The Pull Request API allows you to list, view, edit, create,
    and even merge pull requests. Comments on pull requests
    can be managed via the issues namespace.
    """

    async def list(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[List[GitHubPullRequestModel]]:
        """
         List pull requests

         **Arguments**:

         `repository`

         The repository to return pull requests from, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/pulls#list-pull-requests
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/pulls",
            **kwargs,
        )
        response.data = [GitHubPullRequestModel(data) for data in response.data]
        return response
