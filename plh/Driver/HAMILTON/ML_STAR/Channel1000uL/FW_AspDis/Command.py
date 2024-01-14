import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandActionBase
from plh.driver.tools import CommandBackendErrorHandlingMixin, CommandOptionsListMixin

from .options import OptionsList


@dataclasses.dataclass(kw_only=True)
class Command(
    CommandOptionsListMixin[OptionsList],
    HamiltonCommandActionBase,
    CommandBackendErrorHandlingMixin,
):
    ...
