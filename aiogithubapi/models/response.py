"""GitHub response data class."""
# pylint: disable=protected-access
from __future__ import annotations

from typing import Any, Dict, Generic

from aiohttp.client import ClientResponse
from yarl import URL

from ..const import GenericType, HttpStatusCode
from .base import GitHubDataModelBase


class GitHubResponseHeadersModel(GitHubDataModelBase):
    """GitHub response header model."""

    access_control_allow_origin: str | None = None
    access_control_expose_headers: str | None = None
    cache_control: str | None = None
    content_encoding: str | None = None
    content_security_policy: str | None = None
    content_length: str | None = None
    content_type: str | None = None
    date: str | None = None
    etag: str | None = None
    github_authentication_token_expiration: str | None = None
    last_modified: str | None = None
    link: str | None = None
    referrer_policy: str | None = None
    server: str | None = None
    strict_transport_security: str | None = None
    transfer_encoding: str | None = None
    vary: str | None = None
    retry_after: str | None = None
    expect_ct: str | None = None
    x_accepted_oauth_scopes: str | None = None
    x_commonmarker_version: str | None = None
    x_content_type_options: str | None = None
    x_frame_options: str | None = None
    x_github_media_type: str | None = None
    x_github_request_id: str | None = None
    x_oauth_client_id: str | None = None
    x_oauth_scopes: str | None = None
    x_ratelimit_limit: str | None = None
    x_ratelimit_remaining: str | None = None
    x_ratelimit_reset: str | None = None
    x_ratelimit_resource: str | None = None
    x_ratelimit_used: str | None = None
    x_xss_protection: str | None = None


class GitHubResponseModel(GitHubDataModelBase, Generic[GenericType]):
    """GitHub response data class."""

    _process_data: bool = False
    _raw_data: ClientResponse
    _slugify_keys: bool = True

    headers: GitHubResponseHeadersModel = None
    status: HttpStatusCode = None
    data: GenericType | None = None

    def __post_init__(self):
        """Post init."""
        self.headers = GitHubResponseHeadersModel(self._raw_data.headers)
        self.status = self._raw_data.status

    @property
    def etag(self) -> str | None:
        """Return the ETag for this response."""
        return self.headers.etag

    @property
    def pages(self) -> Dict[str, int]:
        """Return the pages for this response."""
        return {
            key: int(self._raw_data.links[key]["url"].query.get("page"))
            for key in self._raw_data.links
        }

    @property
    def is_last_page(self) -> bool:
        """Return True if this is the last page of results."""
        if self.headers.link is None:
            return True
        return self.page_number == self.pages.get("last", self.page_number)

    @property
    def page_number(self) -> int:
        """Return the current page number."""
        if self.headers.link is None:
            return 1
        if previous_page := self.pages.get("prev"):
            return previous_page + 1
        return 1

    @property
    def next_page_number(self) -> int | None:
        """Return the current page number."""
        if self.headers.link is None:
            return None
        return self.pages.get("next", None)

    @property
    def last_page_number(self) -> int | None:
        """Return the current page number."""
        if self.headers.link is None:
            return None
        return self.pages.get("last", None)
