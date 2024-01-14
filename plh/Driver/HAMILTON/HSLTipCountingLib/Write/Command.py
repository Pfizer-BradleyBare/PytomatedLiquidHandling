import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandStateBase
from plh.driver.tools import CommandOptionsListMixin

from .Options import ListedOptions


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListMixin[ListedOptions], HamiltonCommandStateBase):
    ...
