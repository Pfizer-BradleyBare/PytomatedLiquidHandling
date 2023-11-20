from dataclasses import dataclass
from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    TrackNumber: int
