"""AioGithub: Constants"""
BASE_URL = "https://api.github.com"
BASE_HEADERS = {
    "Accept": "application/vnd.github.v3.raw+json",
    "User-Agent": "python/AIOGitHub",
}
GOOD_HTTP_CODES = [200, 201, 202, 203]
