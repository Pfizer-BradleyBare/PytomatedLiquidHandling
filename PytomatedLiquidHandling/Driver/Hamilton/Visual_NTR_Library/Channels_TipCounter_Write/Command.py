from pydantic import dataclasses

from ....Tools.BaseClasses import CommandOptionsListed
from ...Backend import HamiltonStateCommandABC
from .Options import ListedOptions


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListed[ListedOptions], HamiltonStateCommandABC):
    ...
