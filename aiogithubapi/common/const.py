"""AIOGitHubAPI: Constants"""
ACCEPT_HEADERS = {
    "base": "application/vnd.github.v3.raw+json",
    "preview": "application/vnd.github.mercy-preview+json",
}

BASE_API_HEADERS = {
    "Accept": ACCEPT_HEADERS["base"],
    "User-Agent": "python/AIOGitHubAPI",
}

BASE_API_URL = "https://api.github.com"


# Status codes
HTTP_STATUS_CODE_OK = 200
HTTP_STATUS_CODE_CREATED = 201
HTTP_STATUS_CODE_ACCEPTED = 202
HTTP_STATUS_CODE_NON_AUTHORITATIVE = 203
HTTP_STATUS_CODE_RATELIMIT = 403
HTTP_STATUS_CODE_TEAPOT = 418

HTTP_STATUS_CODE_GOOD_LIST = [
    HTTP_STATUS_CODE_OK,
    HTTP_STATUS_CODE_CREATED,
    HTTP_STATUS_CODE_ACCEPTED,
    HTTP_STATUS_CODE_NON_AUTHORITATIVE,
]
