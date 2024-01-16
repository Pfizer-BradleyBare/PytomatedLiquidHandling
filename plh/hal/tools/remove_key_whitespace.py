from __future__ import annotations

from typing import Any


def remove_key_whitespace(json: dict | list) -> Any:
    if isinstance(json, dict):
        return {
            k.replace("\n", "").replace(" ", ""): remove_key_whitespace(v)
            for k, v in json.items()
        }
    if isinstance(json, list):
        return [remove_key_whitespace(item) for item in json]

    return json
