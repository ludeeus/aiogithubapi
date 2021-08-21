"""Initialise aiogithubapi models."""
from .base import GitHubBase
from .clones import GitHubClonesModel
from .commit import GitHubCommitModel
from .contents import GitHubContentsModel
from .device_login import GitHubLoginDeviceModel
from .git_tree import GitHubGitTreeModel
from .issue import GitHubIssueModel
from .issue_comment import GitHubIssueCommentModel
from .label import GitHubLabelModel
from .license import GitHubLicenseModel
from .login_oauth import GitHubLoginOauthModel
from .milestone import GitHubMilestoneModel
from .organization import GitHubOrganizationModel
from .owner import GitHubOwnerModel
from .permissions import GitHubPermissionsModel
from .pull_request import GitHubPullRequestModel
from .rate_limit import (
    GitHubRateLimitModel,
    GitHubRateLimitResourceModel,
    GitHubRateLimitResourcesModel,
)
from .reaction import GitHubReactionModel
from .release import GitHubReleaseAssetModel, GitHubReleaseModel
from .repository import GitHubRepositoryModel
from .request_data import GitHubBaseRequestDataModel
from .response import GitHubResponseHeadersModel, GitHubResponseModel
from .user import (
    GitHubAuthenticatedUserModel,
    GitHubBaseUserModel,
    GitHubUserModel,
    GitHubUserPlanModel,
)
from .views import GitHubViewsModel
