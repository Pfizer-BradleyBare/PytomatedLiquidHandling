import dataclasses

from ....Tools.BaseClasses import CommandOptions
from ...Backend import HamiltonStateCommandABC
from .Options import Options


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptions[Options], HamiltonStateCommandABC):
    ...
