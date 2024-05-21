"""Test repository dataclass."""
from io import BytesIO
import json
from unittest.mock import patch
from aiogithubapi import Repository
from aiogithubapi.helpers import repository_full_name, sigstore_verify_release_asset
from sigstore.verify import VerificationSuccess, VerificationFailure


def test_repository():
    """Test repository dataclass."""
    assert (
        repository_full_name(Repository(owner="octocat", repo="Hello-World"))
        == "octocat/Hello-World"
    )
    assert repository_full_name("octocat/Hello-World") == "octocat/Hello-World"
    assert (
        repository_full_name({"owner": "octocat", "repo": "Hello-World"}) == "octocat/Hello-World"
    )


def test_sigstore_success():
    with patch("sigstore.verify.Verifier.verify", return_value=VerificationSuccess()), patch(
        "sigstore.verify.VerificationMaterials.from_bundle"
    ):
        verification = sigstore_verify_release_asset(
            asset=b"test",
            signature_bundle=bytes(json.dumps({"critical": {"identity": "test"}}), "utf-8"),
            repository="test",
            workflow="test",
            tag="test",
            workflow_name="test",
            workflow_trigger="release",
        )
        assert verification.success
        assert getattr(verification, "reason", None) is None
        assert verification.success is True


def test_sigstore_failure():
    with patch(
        "sigstore.verify.Verifier.verify",
        return_value=VerificationFailure(reason="Some reason"),
    ), patch("sigstore.verify.VerificationMaterials.from_bundle"):
        verification = sigstore_verify_release_asset(
            asset=b"test",
            signature_bundle=bytes(json.dumps({"critical": {"identity": "test"}}), "utf-8"),
            repository="test",
            workflow="test",
            tag="test",
            workflow_name="test",
            workflow_trigger="release",
        )
        assert getattr(verification, "reason", None) is not None
        assert verification.reason == "Some reason"
        assert verification.success is False
