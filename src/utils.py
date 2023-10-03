import shortuuid


def generate_uid(
    len: int = 12, alphabet: str = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
) -> str:
    su = shortuuid.ShortUUID(alphabet=alphabet)
    return su.random(len)
