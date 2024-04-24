from __future__ import annotations

import dataclasses
from typing import Any

from plh.device.tools import CommandOptionsListMixin
from plh.device.UnchainedLabs_Instruments.backend import UnchainedLabsCommandBase

from .options import OptionsList


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandBase, CommandOptionsListMixin[OptionsList]):
    def execute_command_helper(self: Command, stunner_dll_object) -> Any:
        results_definition = "[Export results]"
        results_definition += "\n"
        results_definition += (
            f'column_names="{";".join([Opt.value for Opt in self.options])}"'
        )
        results_definition += "\n"
        results_definition += "separator=,"
        results_definition += "\n"
        results_definition += 'undefined_column_name="remove"'
        results_definition += "\n"
        results_definition += f'no_result_value="{self.options.NoResultValue}"'
        results_definition += "\n"

        return {
            "status_code_raw": 0,
            "results_definition": results_definition,
        }
