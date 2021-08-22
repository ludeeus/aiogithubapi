"""
Methods for the contents namespace

https://docs.github.com/en/rest/reference/repos#contents
"""
from __future__ import annotations

from typing import Any, Dict

from aiohttp.hdrs import ACCEPT

from ..const import GitHubRequestAcceptHeader, GitHubRequestKwarg, RepositoryType
from ..helpers import repository_full_name
from ..models.contents import GitHubContentsModel
from ..models.response import GitHubResponseModel
from .base import BaseNamespace


class GitHubContentsNamespace(BaseNamespace):
    """Methods for the contents namespace"""

    async def get(
        self,
        repository: RepositoryType,
        path: str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubContentsModel | list[GitHubContentsModel]]:
        """
         Get repository content

        Gets the contents of a file or directory in a repository.

        Files and symlinks support a custom media type for retrieving the raw content
        or rendered HTML (when supported). All content types support a custom media
        type to ensure the content is returned in a consistent object format.

         **Arguments**:

         `repository`

         The repository to return contents from, example "octocat/hello-world"

         `path`

         Specify the file path or directory. If you omit this, you will
         receive the contents of the repository's root directory.

        https://docs.github.com/en/rest/reference/repos#get-repository-content
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}"
            f"/contents{f'/{path}' if path else ''}",
            **{
                GitHubRequestKwarg.HEADERS: {ACCEPT: GitHubRequestAcceptHeader.BASE_JSON},
                **kwargs,
            },
        )

        if isinstance(response.data, list):
            response.data = [GitHubContentsModel(data) for data in response.data]
        else:
            response.data = GitHubContentsModel(response.data)
        return response
