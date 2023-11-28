from dataclasses import dataclass
from typing import Any

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import CommandOptionsListed

from ..Backend import UnchainedLabsCommandABC
from .Options import ListedOptions


@dataclass(kw_only=True)
class Command(UnchainedLabsCommandABC, CommandOptionsListed[ListedOptions]):
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        ResultsDefinition = "[Export results]"
        ResultsDefinition += "\n"
        ResultsDefinition += (
            f'column_names="{";".join([Opt.value for Opt in self.Options])}"'
        )
        ResultsDefinition += "\n"
        ResultsDefinition += f"separator={self.Options.Separator}"
        ResultsDefinition += "\n"
        ResultsDefinition += 'undefined_column_name="remove"'
        ResultsDefinition += "\n"
        ResultsDefinition += f'no_result_value="{self.Options.NoResultValue}"'
        ResultsDefinition += "\n"

        Result = StunnerDLLObject.Get_Results(
            ResultsDefinition, "", "",""
        )

        return dict(StatusCode=Result[0], Results=Result[1], ResultsPath=Result[2])
