from dataclasses import dataclass

from .....Tools.BaseClasses import CommandOptionsListed
from ....Backend import HamiltonActionCommandABC
from .Options import ListedOptions


@dataclass(kw_only=True)
class Command(CommandOptionsListed[ListedOptions], HamiltonActionCommandABC):
    BackendErrorHandling: bool
