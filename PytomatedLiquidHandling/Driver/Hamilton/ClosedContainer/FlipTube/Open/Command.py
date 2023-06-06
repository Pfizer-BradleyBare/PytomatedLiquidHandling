from .....Tools.AbstractClasses import CommandOptionsTracker
from ....Backend import HamiltonActionCommandABC
from .OptionsTracker import OptionsTracker
from dataclasses import dataclass


@HamiltonActionCommandABC.Decorator_Command(__file__)
@dataclass
class Command(CommandOptionsTracker[OptionsTracker], HamiltonActionCommandABC):
    ...
