import dataclasses

from plh.device.HAMILTON.backend import HamiltonCommandActionBase
from plh.device.tools import CommandOptionsListMixin

from .options import OptionsList


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListMixin[OptionsList], HamiltonCommandActionBase): ...
