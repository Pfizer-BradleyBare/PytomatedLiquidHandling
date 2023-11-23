from dataclasses import dataclass

from ....Tools.AbstractClasses import CommandOptions
from ...Backend import HamiltonActionCommandABC


@dataclass(kw_only=True)
class Command(HamiltonActionCommandABC):
    ...
