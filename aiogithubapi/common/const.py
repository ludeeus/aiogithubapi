"""AIOGitHubAPI: Constants"""
from enum import Enum

ACCEPT_HEADERS = {
    "base": "application/vnd.github.v3.raw+json",
    "preview": "application/vnd.github.mercy-preview+json",
}

BASE_API_HEADERS = {
    "Accept": ACCEPT_HEADERS["base"],
    "Content-Type": "application/json",
    "User-Agent": "python/AIOGitHubAPI",
}

BASE_API_URL = "https://api.github.com"
OAUTH_DEVICE_LOGIN = "https://github.com/login/device/code"
OAUTH_USER_LOGIN = "https://github.com/login/device"
OAUTH_ACCESS_TOKEN = "https://github.com/login/oauth/access_token"


class HttpStatusCode(int, Enum):
    """HTTP Status codes."""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE = 203
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    UNAUTHORIZED = 401
    RATELIMIT = 403
    NOT_FOUND = 404
    TEAPOT = 418
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class HttpMethod(str, Enum):
    """HTTP Methods."""

    GET = "GET"
    POST = "POST"


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


HTTP_STATUS_CODE_GOOD_LIST = [
    HttpStatusCode.OK,
    HttpStatusCode.CREATED,
    HttpStatusCode.ACCEPTED,
    HttpStatusCode.NON_AUTHORITATIVE,
]
