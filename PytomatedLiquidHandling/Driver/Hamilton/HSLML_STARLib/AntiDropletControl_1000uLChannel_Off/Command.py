from dataclasses import dataclass

from ....Tools.BaseClasses import CommandOptions
from ...Backend import HamiltonActionCommandABC


@dataclass(kw_only=True)
class Command(HamiltonActionCommandABC):
    ...
