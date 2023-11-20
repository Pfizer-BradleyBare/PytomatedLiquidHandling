from ....Tools.AbstractClasses import CommandOptions
from ...Backend import HamiltonActionCommandABC
from .Options import Options
from dataclasses import dataclass


@dataclass
class Command(CommandOptions[Options], HamiltonActionCommandABC):
    ...
