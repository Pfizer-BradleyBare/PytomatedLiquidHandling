from .....Tools.AbstractClasses import NonUniqueObjectABC
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class OptionsABC(NonUniqueObjectABC):
    Identifier: str | int = field(default="None")
