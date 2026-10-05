"""In-process catalog search over ats-agent skill/tech alias dictionaries."""

from __future__ import annotations

from typing import Any


def humanize_key(key: str) -> str:
    """Turn snake_case catalog ids into readable labels."""
    return key.replace("_", " ").strip()


def search_catalog(
    catalog: dict[str, list[str]],
    *,
    q: str | None = None,
    limit: int = 40,
    kind_by_id: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Search canonical keys and aliases; return list payload plus legacy keys/aliases.

    Ranking preference when ``q`` is set:
    1. Exact canonical key match
    2. Canonical key substring
    3. Exact alias match
    4. Alias substring
    """
    keys = sorted(catalog.keys(), key=str.lower)
    aliases = {k: list(catalog.get(k) or []) for k in keys}
    query = (q or "").strip().lower()
    capped = max(1, min(int(limit or 40), 100))

    if not query:
        items = [
            {
                "id": key,
                "label": humanize_key(key),
                **({"kind": kind_by_id[key]} if kind_by_id and key in kind_by_id else {}),
            }
            for key in keys[:capped]
        ]
        return {"items": items, "keys": keys, "aliases": aliases}

    scored: list[tuple[int, str, str | None]] = []
    for key, alias_list in aliases.items():
        key_l = key.lower()
        label_l = humanize_key(key).lower()
        matched_via: str | None = None
        rank: int | None = None

        if query == key_l or query == label_l:
            rank = 0
        else:
            for alias in alias_list:
                alias_l = str(alias).lower()
                if query == alias_l:
                    rank = 1
                    matched_via = str(alias)
                    break
            if rank is None:
                if query in key_l or query in label_l:
                    rank = 2
                else:
                    for alias in alias_list:
                        alias_l = str(alias).lower()
                        if query in alias_l:
                            rank = 3
                            matched_via = str(alias)
                            break

        if rank is None:
            continue
        scored.append((rank, key, matched_via))

    scored.sort(key=lambda row: (row[0], row[1].lower()))
    items = []
    for _rank, key, matched_via in scored[:capped]:
        item: dict[str, Any] = {
            "id": key,
            "label": humanize_key(key),
        }
        if matched_via and matched_via.lower() != key.lower() and matched_via.lower() != humanize_key(key).lower():
            item["matched_via"] = matched_via
        if kind_by_id and key in kind_by_id:
            item["kind"] = kind_by_id[key]
        items.append(item)

    return {"items": items, "keys": keys, "aliases": aliases}


def resolve_to_canonical(catalog: dict[str, list[str]], value: str) -> str:
    """Map a typed value (canonical or alias) to its catalog key when possible."""
    raw = (value or "").strip()
    if not raw:
        return raw
    lower = raw.lower()
    for key, alias_list in catalog.items():
        if lower == key.lower() or lower == humanize_key(key).lower():
            return key
        for alias in alias_list:
            if lower == str(alias).lower():
                return key
    return raw
