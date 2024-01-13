import dataclasses

from ....Tools.BaseClasses import CommandOptions
from ...Backend import HamiltonActionCommandABC


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonActionCommandABC):
    ...
