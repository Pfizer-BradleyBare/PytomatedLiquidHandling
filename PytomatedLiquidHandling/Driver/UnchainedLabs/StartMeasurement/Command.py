from dataclasses import dataclass
from typing import Any

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import CommandOptions

from ..Backend import UnchainedLabsCommandABC
from .Options import Options

@dataclass(kw_only=True)
class Command(UnchainedLabsCommandABC, CommandOptions[Options]):
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        import clr
        from System import String #type:ignore

        return dict(StatusCode=StunnerDLLObject.Measure.__overloads__[String](self.Options.PlateID))
        #Pythonnet allows us to select the specific overload. In this case there are two:
        # 1. Input string
        # 2. Output string
        # By default the output string is selected. The overload above selects the input string overload.
