"""Fixtures."""
# pylint: disable=missing-docstring
import pytest


@pytest.fixture()
def base_response():
    return {"key": "value"}
