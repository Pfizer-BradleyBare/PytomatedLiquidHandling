from dataclasses import dataclass

from .....Tools.AbstractClasses import CommandOptionsListed
from ....Backend import HamiltonStateCommandABC
from .Options import ListedOptions


@dataclass
class Command(CommandOptionsListed[ListedOptions], HamiltonStateCommandABC):
    ...
