import dataclasses

from ....Tools.BaseClasses import CommandOptionsListed
from ...Backend import HamiltonStateCommandABC
from .Options import Options


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListed[list[Options]], HamiltonStateCommandABC):
    ...
