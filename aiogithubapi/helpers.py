def short_sha(sha: str) -> str:
    return sha[0:7]


def short_message(message: str) -> str:
    return message.split("\n")[0]
