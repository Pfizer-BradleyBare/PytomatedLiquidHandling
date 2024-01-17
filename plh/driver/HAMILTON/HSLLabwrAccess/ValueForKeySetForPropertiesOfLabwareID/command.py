import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandStateBase
from plh.driver.tools import CommandOptionsListMixin

from .options import OptionsList


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListMixin[OptionsList], HamiltonCommandStateBase):
    ...
