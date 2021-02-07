"""Common variables for testing."""
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLIENT_ID = "xxxxxx"
NOT_RATELIMITED = {
    "X-RateLimit-Remaining": "1337",
    "Content-Type": "application/json",
    "ETag": "xyz..zyx",
}
RATELIMITED = {"X-RateLimit-Remaining": "0", "Content-Type": "application/json"}
