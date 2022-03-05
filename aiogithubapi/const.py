"""Constants for aiogithubapi."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from logging import Logger, getLogger
from typing import Dict, Literal, TypeVar, Union

from aiohttp.hdrs import ACCEPT, CONTENT_TYPE, USER_AGENT

GenericType = TypeVar("GenericType")

PROJECT_VERSION = "main"
PROJECT_NAME = "aiogithubapi"
PROJECT_URL = "https://github.com/ludeeus/aiogithubapi"

# Deprecated, use `GitHubRequestAcceptHeader` instead
ACCEPT_HEADERS: Dict[str, str] = {
    "base": "application/vnd.github.v3.raw+json",
    "preview": "application/vnd.github.mercy-preview+json",
}

# This is the default user agent,
# but it is adviced to use your own when building out your application
DEFAULT_USER_AGENT = f"aiogithubapi/{PROJECT_VERSION}"

BASE_API_URL = "https://api.github.com"
BASE_GITHUB_URL = "https://github.com"
OAUTH_DEVICE_LOGIN_PATH = "/login/device/code"
OAUTH_ACCESS_TOKEN_PATH = "/login/oauth/access_token"
OAUTH_USER_LOGIN = "https://github.com/login/device"


LOGGER: Logger = getLogger(PROJECT_NAME)


@dataclass
class Repository:
    """Repository."""

    owner: str
    repo: str

    @property
    def full_name(self) -> str:
        """Full name."""
        return f"{self.owner}/{self.repo}"


RepositoryType = Union[str, Dict[Literal["owner", "repo"], str], Repository]


class GitHubRequestAcceptHeader(str, Enum):
    """
    GitHub uses vaious accept headers to enable certain features.

    https://docs.github.com/en/rest/overview/media-types
    """

    RAW_JSON = "application/vnd.github.v3.raw+json"
    BASE_JSON = "application/vnd.github.v3+json"
    PREVIEW_MERCY = "application/vnd.github.mercy-preview+json"

    BASE = RAW_JSON
    PREVIEW = PREVIEW_MERCY


class GitHubClientKwarg(str, Enum):
    """
    kwargs that are used by the client.

    These are used to construct the client and will affect all requests.

    HEADERS:
        Used to set the base headers for all requests.
    BASE_URL:
        Used to ovveride the base url for all requests. Defaults to https://api.github.com .
    TIMEOUT:
        Used to set the timeout for all requests. Defaults to 20
    CLIENT_NAME:
        This name will be used as the user agent header.
    """

    HEADERS = "headers"
    BASE_URL = "base_url"
    TIMEOUT = "timeout"
    CLIENT_NAME = "client_name"


class GitHubRequestKwarg(str, Enum):
    """
    kwargs that are used by requests.

    ETAG:
        Used to set the IF_NONE_MATCH header, if this is set and the content
        is not modified GitHubNotModifiedException will be raised.
    HEADERS:
        Used to set the headers of the request.
    METHOD:
        Used to set the method of the request. Defaults to GET.
    PARAMS:
        Used to set the params of the request.
    QUERY:
        Alias for PARAMS.
    SCOPE:
        Only used for github device login to request scopes for the token
    """

    ETAG = "etag"
    HEADERS = "headers"
    METHOD = "method"
    PARAMS = "params"
    QUERY = "query"
    SCOPE = "scope"


class HttpStatusCode(int, Enum):
    """HTTP Status codes."""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE = 203
    NO_CONTENT = 204
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    RATELIMIT = 403
    FORBIDDEN = 403
    NOT_FOUND = 404
    TEAPOT = 418
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class GitHubIssueLockReason(str, Enum):
    """Reason for issue lock."""

    OFF_TOPIC = "off-topic"
    SPAM = "spam"
    TOO_HEATED = "too heated"
    RESOLVED = "resolved"


class HttpMethod(str, Enum):
    """HTTP Methods."""

    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"
    PUT = "PUT"


class HttpContentType(str, Enum):
    """HTTP Content Types."""

    BASE_JSON = "application/json"
    BASE_ZIP = "application/zip"
    BASE_GZIP = "application/x-gzip"

    JSON = "application/json;charset=utf-8"
    TEXT_PLAIN = "text/plain;charset=utf-8"
    TEXT_HTML = "text/html;charset=utf-8"


class DeviceFlowError(str, Enum):
    """
    Errors for Device Flow.

    https://docs.github.com/en/developers/apps/authorizing-oauth-apps#error-codes-for-the-device-flow
    """

    ACCESS_DENIED = "access_denied"
    AUTHORIZATION_PENDING = "authorization_pending"
    EXPIRED_TOKEN = "expired_token"
    INCORRECT_CLIENT_CREDENTIALS = "incorrect_client_credentials"
    INCORRECT_DEVICE_CODE = "incorrect_device_code"
    SLOW_DOWN = "slow_down"
    UNSUPPORTED_GRANT_TYPE = "unsupported_grant_type"


HTTP_STATUS_CODE_GOOD_LIST: list[HttpStatusCode] = [
    HttpStatusCode.OK,
    HttpStatusCode.CREATED,
    HttpStatusCode.ACCEPTED,
    HttpStatusCode.NON_AUTHORITATIVE,
]


BASE_API_HEADERS: Dict[str, str] = {
    ACCEPT: GitHubRequestAcceptHeader.BASE.value,
    CONTENT_TYPE: HttpContentType.JSON.value,
    USER_AGENT: DEFAULT_USER_AGENT,
}
