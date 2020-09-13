"""AIOGitHubAPI: Constants"""
from enum import Enum

VERSION = "0.0.0"

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
    UNAUTHORIZED = 401
    RATELIMIT = 403
    NOT_FOUND = 404
    TEAPOT = 418
    INTERNAL_SERVER_ERROR = 500


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


HTTP_STATUS_CODE_OK = 200
HTTP_STATUS_CODE_CREATED = 201
HTTP_STATUS_CODE_ACCEPTED = 202
HTTP_STATUS_CODE_NON_AUTHORITATIVE = 203
HTTP_STATUS_CODE_RATELIMIT = 403
HTTP_STATUS_CODE_TEAPOT = 418

HTTP_STATUS_CODE_GOOD_LIST = [200, 201, 202, 203]
