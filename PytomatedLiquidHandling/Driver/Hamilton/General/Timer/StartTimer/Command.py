from dataclasses import dataclass

from .....Tools.AbstractClasses import CommandOptions
from ....Backend import HamiltonActionCommandABC
from .Options import Options


@dataclass(kw_only=True)
class Command(CommandOptions[Options], HamiltonActionCommandABC):
    ...
