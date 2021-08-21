"""
Methods for the releases namespace

https://docs.github.com/en/rest/reference/repos#releases
"""
from __future__ import annotations

from typing import Any, List

from ..const import GitHubRequestKwarg, RepositoryType
from ..models import GitHubReleaseModel, GitHubResponseModel
from .base import BaseNamespace


class GitHubReleasesNamespace(BaseNamespace):
    """Methods for the releases namespace"""

    async def list(
        self,
        repository: RepositoryType,
        **kwargs: dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[List[GitHubReleaseModel]]:
        """
        List releases

        This returns a list of releases, which does not include
        regular Git tags that have not been associated with a release.

         **Arguments**:

         `repository`

         The repository to return the tree for, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/repos#list-releases
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository}/releases",
            **kwargs,
        )
        response.data = [GitHubReleaseModel(data) for data in response.data]
        return response
