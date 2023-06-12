from dataclasses import dataclass

from .....Tools.AbstractClasses import CommandOptions
from ....Backend import HamiltonActionCommandABC
from .Options import Options


@dataclass
class Command(CommandOptions[Options], HamiltonActionCommandABC):
    ...
