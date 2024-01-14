import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandActionBase


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandActionBase):
    ...
