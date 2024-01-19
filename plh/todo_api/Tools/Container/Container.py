from dataclasses import dataclass, field

from .Well import Well


@dataclass
class Container:
    Name: str
    Wells: list[Well] = field(init=False)

    def __init__(self, Name: str, NumWells: int):
        self.Name = Name

        for _ in range(0, NumWells):
            self.Wells.append(Well())
