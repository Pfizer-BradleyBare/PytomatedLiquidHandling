from dataclasses import dataclass
from typing import Any

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import CommandOptions

from ..Backend import UnchainedLabsCommandABC
from .Options import Options

@dataclass(kw_only=True)
class Command(UnchainedLabsCommandABC, CommandOptions[Options]):
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        return dict(StatusCode=StunnerDLLObject.Measure(self.Options.PlateID))
