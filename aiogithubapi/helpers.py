"""Helpers for AIOGitHubAPI."""
from __future__ import annotations

from io import BytesIO
from typing import Optional

import aiohttp
from sigstore.verify import (
    VerificationMaterials,
    VerificationResult,
    Verifier,
    models,
    policy,
)

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


def sigstore_verify_downloaded_release_asset(
    asset: bytes,
    signature_bundle: bytes,
    repository: str,
    workflow: str,
    tag: str,
    *,
    workflow_name: str | None = None,
    workflow_trigger: str | None = None,
    offline_verification: bool = False,
    **kwargs,
) -> VerificationResult:
    """Verify release asset."""
    verifier = Verifier.production()
    policies = [
        policy.Identity(
            identity=f"https://github.com/{repository}/.github/workflows/{workflow}@refs/tags/{tag}",
            issuer="https://token.actions.githubusercontent.com",
        ),
        policy.GitHubWorkflowRepository(repository),
        policy.GitHubWorkflowRef(f"refs/tags/{tag}"),
    ]
    if workflow_trigger:
        policies.append(policy.GitHubWorkflowTrigger(workflow_trigger))
    if workflow_name:
        policies.append(policy.GitHubWorkflowName(workflow_name))

    return verifier.verify(
        VerificationMaterials.from_bundle(
            input_=BytesIO(asset),
            bundle=models.Bundle().from_json(signature_bundle),
            offline=offline_verification,
        ),
        policy=policy.AllOf(policies),
    )
