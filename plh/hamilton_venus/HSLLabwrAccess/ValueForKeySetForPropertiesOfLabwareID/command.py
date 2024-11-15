import dataclasses

from plh.hamilton_venus.backend import HamiltonCommandStateBase
from plh.tools import CommandOptionsListMixin

from .options import OptionsList


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListMixin[OptionsList], HamiltonCommandStateBase): ...
