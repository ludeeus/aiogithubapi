"""GitHub Activity event models"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class _Actor(BaseModel):
    """Internal entry."""

    id: str
    login: str
    display_login: str
    gravatar_id: str
    url: str
    avatar_url: str


class _Repo(BaseModel):
    """Internal entry."""

    id: str
    name: str
    url: str


class GitHubEventModel(BaseModel):
    """
    GitHub base event data class.

    The type is PascalCase

    https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types
    """

    id: str
    type: str
    actor: _Actor
    org: _Actor
    repo: _Repo
    payload: dict[str, Any]
    public: bool
    created_at: str
