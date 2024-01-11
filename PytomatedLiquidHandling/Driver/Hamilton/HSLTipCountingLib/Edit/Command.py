import dataclasses

from ....Tools.BaseClasses import CommandOptionsListed
from ...Backend import HamiltonActionCommandABC
from .Options import ListedOptions


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListed[ListedOptions], HamiltonActionCommandABC):
    ...
