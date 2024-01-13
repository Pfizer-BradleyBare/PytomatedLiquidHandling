import dataclasses

from .hamilton_command_base import HamiltonCommandBase


@dataclasses.dataclass(kw_only=True)
class HamiltonCommandStateBase(HamiltonCommandBase):
    ...
