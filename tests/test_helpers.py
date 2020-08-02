from aiogithubapi.helpers import short_sha, short_message


def test_short_sha():
    assert short_sha("123456789") == "1234567"


def test_short_message():
    assert short_message("show\nno show") == "show"
