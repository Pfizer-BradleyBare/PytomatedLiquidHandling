from pydantic import dataclasses

from .....Tools.BaseClasses import CommandBackendErrorHandling, CommandOptionsListed
from ....Backend import HamiltonActionCommandABC
from .Options import ListedOptions


@dataclasses.dataclass(kw_only=True)
class Command(
    CommandOptionsListed[ListedOptions],
    HamiltonActionCommandABC,
    CommandBackendErrorHandling,
):
    ...
