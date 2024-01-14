import dataclasses

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import CommandOptionsMixin

from ..Backend import UnchainedLabsCommandABC
from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandABC, CommandOptionsMixin[Options]):
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        from System import String  # type:ignore

        PlateID = self.Options.PlateID
        if PlateID is None:
            StatusCode, PlateID = StunnerDLLObject.Measure()

        else:
            PlateID = PlateID
            StatusCode = StunnerDLLObject.Measure.__overloads__[String](PlateID)

        # Pythonnet allows us to select the specific overload. In this case there are two:
        # 1. Input string
        # 2. Output string
        # By default the output string is selected. The overload above selects the input string overload.

        return dict(StatusCode=StatusCode, PlateID=PlateID)
