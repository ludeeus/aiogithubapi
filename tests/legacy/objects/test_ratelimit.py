# pylint: disable=missing-docstring, redefined-outer-name, unused-import
from aiogithubapi.objects.ratelimit import AIOGitHubAPIRateLimit


def test_ratelimit():
    ratelimit = AIOGitHubAPIRateLimit()
    assert ratelimit.reset_utc is None
    ratelimit.load_from_response_headers(
        {
            "X-RateLimit-Remaining": "4999",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": "4999",
        }
    )
    assert ratelimit.reset_utc.year == 1970
    assert ratelimit.reset_utc.month == 1
    assert ratelimit.reset_utc.day == 1
    assert ratelimit.reset_utc.hour == 1
    assert ratelimit.reset_utc.minute == 23
    assert ratelimit.reset_utc.second == 19
