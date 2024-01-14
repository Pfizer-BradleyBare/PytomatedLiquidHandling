import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandStateBase
from plh.driver.tools import CommandOptionsMixin

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsMixin[Options], HamiltonCommandStateBase):
    ...
