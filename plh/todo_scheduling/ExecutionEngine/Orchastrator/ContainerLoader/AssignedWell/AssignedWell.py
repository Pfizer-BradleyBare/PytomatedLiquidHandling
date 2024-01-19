from dataclasses import dataclass, field

from PytomatedLiquidHandling.Tools.BaseClasses import UniqueObjectABC


@dataclass
class AssignedWell(UniqueObjectABC):
    ContainerName: str | None = field(init=False, default=None)
