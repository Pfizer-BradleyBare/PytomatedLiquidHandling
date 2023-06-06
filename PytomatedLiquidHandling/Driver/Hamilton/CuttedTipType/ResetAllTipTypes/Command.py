from ...Backend import HamiltonActionCommandABC
from dataclasses import dataclass


@HamiltonActionCommandABC.Decorator_Command(__file__)
@dataclass
class Command(HamiltonActionCommandABC):
    ...
