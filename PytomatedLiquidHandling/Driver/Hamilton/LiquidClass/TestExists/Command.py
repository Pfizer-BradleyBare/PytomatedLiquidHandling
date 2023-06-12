from dataclasses import dataclass
from typing import TypeVar

from ....Tools.AbstractClasses import CommandOptionsTracker
from ...Backend import HamiltonActionCommandABC
from .OptionsTracker import OptionsTracker

CommandSelf = TypeVar("CommandSelf", bound="Command")


@dataclass
class Command(CommandOptionsTracker[OptionsTracker], HamiltonActionCommandABC):
    ...
