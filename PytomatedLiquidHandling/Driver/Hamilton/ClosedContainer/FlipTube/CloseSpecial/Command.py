from .....Tools.AbstractClasses import CommandOptionsTracker
from ....Backend import HamiltonActionCommandABC
from .OptionsTracker import OptionsTracker
from dataclasses import dataclass


@dataclass
class Command(CommandOptionsTracker[OptionsTracker], HamiltonActionCommandABC):
    ...
