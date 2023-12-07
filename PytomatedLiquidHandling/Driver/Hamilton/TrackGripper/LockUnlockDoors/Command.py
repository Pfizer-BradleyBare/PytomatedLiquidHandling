from dataclasses import dataclass

from ....Tools.BaseClasses import CommandOptions, CommandBackendErrorHandling
from ...Backend import HamiltonActionCommandABC
from .Options import Options


@dataclass(kw_only=True)
class Command(
    CommandOptions[Options], HamiltonActionCommandABC, CommandBackendErrorHandling
):
    ...
