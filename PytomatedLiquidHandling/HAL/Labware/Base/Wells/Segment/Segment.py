from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Segment:
    Height: float
    Equation: str
