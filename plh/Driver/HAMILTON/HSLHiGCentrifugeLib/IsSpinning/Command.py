import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandStateBase


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandStateBase):
    ...
