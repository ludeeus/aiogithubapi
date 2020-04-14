"""Common variables for testing."""
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
NOT_RATELIMITED = {"X-RateLimit-Remaining": "1337", "Content-Type": "application/json"}
RATELIMITED = {"X-RateLimit-Remaining": "0", "Content-Type": "application/json"}
