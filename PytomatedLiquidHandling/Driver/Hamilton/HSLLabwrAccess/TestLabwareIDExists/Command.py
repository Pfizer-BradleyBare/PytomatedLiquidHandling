from dataclasses import dataclass

from ....Tools.AbstractClasses import CommandOptionsListed
from ...Backend import HamiltonStateCommandABC
from .Options import Options


@dataclass(kw_only=True)
class Command(CommandOptionsListed[list[Options]], HamiltonStateCommandABC):
    ...
