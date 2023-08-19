import secrets


def make_userid():
    userid = secrets.token_bytes(32)
    return userid.hex()
