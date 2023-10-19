from typing import Any


def RemoveKeyWhitespace(Dict) -> Any:
    if isinstance(Dict, dict):
        return {
            k.replace("\n", "").replace(" ", ""): RemoveKeyWhitespace(v)
            for k, v in Dict.items()
        }
    elif isinstance(Dict, list):
        return [RemoveKeyWhitespace(item) for item in Dict]
    else:
        return Dict
