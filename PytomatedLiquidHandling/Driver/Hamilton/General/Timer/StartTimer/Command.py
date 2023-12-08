from pydantic import dataclasses

from .....Tools.BaseClasses import CommandOptions
from ....Backend import HamiltonActionCommandABC
from .Options import Options


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptions[Options], HamiltonActionCommandABC):
    ...
