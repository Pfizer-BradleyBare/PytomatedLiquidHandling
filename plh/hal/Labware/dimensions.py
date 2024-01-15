from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Dimensions:
    XLength: float
    YLength: float
