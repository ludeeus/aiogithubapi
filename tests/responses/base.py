"""Fixtures."""
# pylint: disable=missing-docstring
import pytest


@pytest.fixture()
def base_response():
    return {"key": "value"}


@pytest.fixture()
def bad_auth_response():
    return {"message": "Bad credentials"}


@pytest.fixture()
def bad_response():
    return {"message": "I'm a tea pot", "code": 418}
