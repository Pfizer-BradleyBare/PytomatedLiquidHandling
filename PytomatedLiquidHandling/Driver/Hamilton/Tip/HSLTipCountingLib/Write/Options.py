from dataclasses import dataclass

from .....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    VirtualSequence: list[tuple[str, str]]
