from ....Tools.AbstractClasses import OptionsABC
from dataclasses import dataclass


@dataclass(kw_only=True)
class Options(OptionsABC):
    Sequence: str
    PropertyKey: str
    PropertyValue: str
