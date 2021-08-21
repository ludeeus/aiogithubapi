"""
Asynchronous Python client for the GitHub API https://github.com/ludeeus/aiogithubapi

.. include:: ../documentation.md
"""
from .common.exceptions import (
    AIOGitHubAPIAuthenticationException,
    AIOGitHubAPIException,
    AIOGitHubAPINotModifiedException,
    AIOGitHubAPIRatelimitException,
)
from .const import (
    DeviceFlowError,
    GitHubClientKwarg,
    GitHubIssueLockReason,
    GitHubRequestKwarg,
    HttpStatusCode,
    Repository,
)
from .device import GitHubDeviceAPI
from .exceptions import (
    GitHubAuthenticationException,
    GitHubConnectionException,
    GitHubException,
    GitHubNotModifiedException,
    GitHubRatelimitException,
)
from .github import GitHub as GitHubAPI
from .legacy.device import AIOGitHubAPIDeviceLogin as GitHubDevice
from .legacy.github import AIOGitHubAPI as GitHub
from .models import *

__all__ = (
    "DeviceFlowError",
    "GitHubAPI",
    "GitHubAuthenticationException",
    "GitHubBase",
    "GitHubBaseRequestDataModel",
    "GitHubClientKwarg",
    "GitHubConnectionException",
    "GitHubDeviceAPI",
    "GitHubException",
    "GitHubLoginDeviceModel",
    "GitHubLoginOauthModel",
    "GitHubNotModifiedException",
    "GitHubRatelimitException",
    "GitHubRepositoryModel",
    "GitHubRequestKwarg",
    "GitHubResponseModel",
    "GitHubIssueLockReason",
    "HttpStatusCode",
    "Repository",
    # Deprecated
    "AIOGitHubAPIAuthenticationException",
    "AIOGitHubAPIException",
    "AIOGitHubAPINotModifiedException",
    "AIOGitHubAPIRatelimitException",
    "GitHub",
    "GitHubDevice",
)
