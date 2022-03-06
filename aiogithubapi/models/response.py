"""GitHub response data class."""
# pylint: disable=protected-access
from __future__ import annotations

from typing import Any, Dict, Generic

from aiohttp.client import ClientResponse
from pydantic import BaseModel, root_validator
from yarl import URL

from ..const import GenericType, HttpStatusCode
from .base import GitHubDataModelBase


class GitHubResponseHeadersModel(BaseModel):
    """GitHub response header model."""

    access_control_allow_origin: str | None
    access_control_expose_headers: str | None
    cache_control: str | None
    content_encoding: str | None
    content_security_policy: str | None
    content_length: str | None
    content_type: str | None
    date: str | None
    etag: str | None
    github_authentication_token_expiration: str | None
    last_modified: str | None
    link: str | None
    referrer_policy: str | None
    server: str | None
    strict_transport_security: str | None
    transfer_encoding: str | None
    vary: str | None
    retry_after: str | None
    expect_ct: str | None
    permissions_policy: str | None
    x_accepted_oauth_scopes: str | None
    x_commonmarker_version: str | None
    x_content_type_options: str | None
    x_frame_options: str | None
    x_github_media_type: str | None
    x_github_request_id: str | None
    x_oauth_client_id: str | None
    x_oauth_scopes: str | None
    x_poll_interval: str | None
    x_ratelimit_limit: str | None
    x_ratelimit_remaining: str | None
    x_ratelimit_reset: str | None
    x_ratelimit_resource: str | None
    x_ratelimit_used: str | None
    x_xss_protection: str | None

    @root_validator(pre=True)
    def _convert_keys(cls, values):
        new_values = {}
        for key, value in values.items():
            new_values[key.replace("-", "_").lower()] = value

        return new_values


class GitHubResponseModel(GitHubDataModelBase, Generic[GenericType]):
    """GitHub response data class."""

    _process_data: bool = False
    _raw_data: ClientResponse | None = None
    _slugify_keys: bool = True

    headers: GitHubResponseHeadersModel | None = None
    status: HttpStatusCode | None = None
    data: GenericType | None = None

    def __post_init__(self):
        """Post init."""
        self.headers = GitHubResponseHeadersModel.parse_obj(self._raw_data.headers)
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
