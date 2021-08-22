"""Helpers for AIOGitHubAPI."""
from __future__ import annotations

from typing import Optional

import aiohttp

from .const import HttpMethod, Repository, RepositoryType
from .legacy.helpers import (
    async_call_api as legacy_async_call_api,
    short_message,
    short_sha,
)
from .objects.base import AIOGitHubAPIResponse


def repository_full_name(repository: RepositoryType) -> str:
    """Return the repository name."""
    if isinstance(repository, str):
        return repository
    if isinstance(repository, Repository):
        return repository.full_name
    return f"{repository['owner']}/{repository['repo']}"


async def async_call_api(
    session: aiohttp.ClientSession,
    method: HttpMethod,
    url: str,
    headers: dict,
    params: Optional[dict] = None,
    data: dict or str or None = None,
    jsondata: bool = True,
    returnjson: bool = True,
) -> AIOGitHubAPIResponse:
    """Deprecated: Execute the API call."""
    return await legacy_async_call_api(
        session, method, url, headers, params, data, jsondata, returnjson
    )
