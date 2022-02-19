"""GitHub meta data class."""
from __future__ import annotations

from .base import GitHubDataModelBase


class _FingerPrints(GitHubDataModelBase):
    """Representation of a GitHub tag commit."""

    sha256_rsa: str | None = None
    sha256_dsa: str | None = None
    sha256_ecdsa: str | None = None
    sha256_ed25519: str | None = None


class GitHubMetaModel(GitHubDataModelBase):
    """GitHub meta data class."""

    verifiable_password_authentication: bool | None = None
    ssh_key_fingerprints: _FingerPrints | None = None
    ssh_keys: list[str] | None = None
    hooks: list[str] | None = None
    web: list[str] | None = None
    api: list[str] | None = None
    git: list[str] | None = None
    packages: list[str] | None = None
    pages: list[str] | None = None
    importer: list[str] | None = None
    actions: list[str] | None = None
    dependabot: list[str] | None = None

    def _generate_ssh_key_fingerprints(self, data: dict) -> _FingerPrints:
        """Generate commit data."""
        return _FingerPrints(data)
