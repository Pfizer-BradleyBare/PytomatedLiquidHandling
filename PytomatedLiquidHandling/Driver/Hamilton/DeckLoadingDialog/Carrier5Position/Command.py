from ....Tools.AbstractClasses import CommandOptionsListed
from ...Backend import HamiltonActionCommandABC
from .Options import ListedOptions


from dataclasses import dataclass


@dataclass
class Command(CommandOptionsListed[ListedOptions], HamiltonActionCommandABC):
    ...
