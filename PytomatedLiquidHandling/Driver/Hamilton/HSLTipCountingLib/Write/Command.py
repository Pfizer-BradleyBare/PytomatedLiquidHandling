from dataclasses import dataclass

from ....Tools.AbstractClasses import CommandOptionsListed
from ...Backend import HamiltonStateCommandABC
from .Options import ListedOptions


@dataclass(kw_only=True)
class Command(CommandOptionsListed[ListedOptions], HamiltonStateCommandABC):
    ...
