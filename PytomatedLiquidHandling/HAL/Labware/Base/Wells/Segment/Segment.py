from pydantic.dataclasses import dataclass


@dataclass
class Segment:
    Height: float
    Equation: str
