from .....Tools.AbstractClasses import CommandOptionsListed
from ....Backend import HamiltonActionCommandABC
from .Options import ListedOptions
from dataclasses import dataclass


@dataclass(kw_only=True)
class Command(CommandOptionsListed[ListedOptions], HamiltonActionCommandABC):
    ...
