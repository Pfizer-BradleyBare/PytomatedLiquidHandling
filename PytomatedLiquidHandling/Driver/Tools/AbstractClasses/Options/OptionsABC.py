from dataclasses import dataclass, field

from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectABC


@dataclass(kw_only=True)
class OptionsABC(NonUniqueObjectABC):
    Identifier: str | int = field(default="None")
