import dataclasses
from typing import Any

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import (
    CommandOptionsListMixin,
)

from ..Backend import UnchainedLabsCommandABC
from .options import ListedOptions


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandABC, CommandOptionsListMixin[ListedOptions]):
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

        StatusCode, Results, ResultsPath = StunnerDLLObject.Get_Results(
            ResultsDefinition,
            "",
        )

        return dict(StatusCode=StatusCode, Results=Results, ResultsPath=ResultsPath)