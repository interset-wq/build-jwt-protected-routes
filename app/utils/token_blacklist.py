blacklist = set()


def blacklist_token(token: str) -> None:
    blacklist.add(token)


def is_blacklisted(token: str) -> bool:
    return token in blacklist
