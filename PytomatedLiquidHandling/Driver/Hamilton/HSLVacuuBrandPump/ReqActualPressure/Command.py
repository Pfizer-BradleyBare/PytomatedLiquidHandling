from dataclasses import dataclass

from ....Tools.BaseClasses import CommandOptions
from ...Backend import HamiltonStateCommandABC
from .Options import Options


@dataclass(kw_only=True)
class Command(CommandOptions[Options], HamiltonStateCommandABC):
    ...
