import hashlib
from datetime import datetime

import shortuuid
import slugify


def patch_rows(rows: list[dict], patches: dict) -> list[dict]:
    list(map(lambda r: r.update(patches), rows))
    return rows


def dt_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def inject_branch_uid(branch_uid: str, records: list[dict]) -> list[dict]:
    for r in records:
        r["branch_uid"] = branch_uid.upper()
    return records


def generate_uid(
    len: int = 12, alphabet: str = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
) -> str:
    su = shortuuid.ShortUUID(alphabet=alphabet)
    return su.random(len)


def hashify(inputs: list[str], max_len: int = -1) -> str:
    parts = []
    for s in inputs:
        parts.append(slugify.slugify(s.strip() if s else ""))
    slug = "^".join(parts)
    h = hashlib.md5(slug.encode("utf-8")).hexdigest().upper()
    if max_len > 0:
        return h[:max_len]
    return h


def initials(full_name: str, min_len: int = 8) -> str:
    if full_name:
        full_name = full_name.strip()

    if not full_name:
        return generate_uid(min_len)

    full_name = slugify.slugify(full_name, separator=" ")

    result = "".join([s[0] for s in full_name.split(" ")])

    delta = min_len - len(result)
    if delta > 0:
        result += generate_uid(delta, "23456789")

    return result.lower()
