from dataclasses import dataclass, field

from .Well import Well


@dataclass
class Container:
    Name: str
    Wells: list[Well] = field(init=False)

    def __init__(self, Name: str):
        ...
