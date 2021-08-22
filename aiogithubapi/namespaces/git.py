"""
Methods for the git namespace

https://docs.github.com/en/rest/reference/git
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg, RepositoryType
from ..models.git_tree import GitHubGitTreeModel
from ..models.response import GitHubResponseModel
from .base import BaseNamespace


class GitHubGitNamespace(BaseNamespace):
    """Methods for the git namespace"""

    async def get_tree(
        self,
        repository: RepositoryType,
        tree_sha: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubGitTreeModel]:
        """
        Get a tree
        Returns a single tree using the SHA1 value for that tree.

        If truncated is true in the response then the number of items in
        the tree array exceeded our maximum limit.
        If you need to fetch more items, use the
        non-recursive method of fetching trees, and fetch one sub-tree at a time.

         **Arguments**:

         `repository`

         The repository to return the tree for, example "octocat/hello-world"

         `tree_sha`

         The tree SHA or ref to return

        https://docs.github.com/en/rest/reference/git#get-a-tree
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository}/git/trees/{tree_sha}",
            **kwargs,
        )
        response.data = GitHubGitTreeModel(response.data)
        return response
