from __future__ import annotations

import dataclasses
from typing import Any

from plh.driver.tools import CommandOptionsMixin
from plh.driver.UnchainedLabs.backend import UnchainedLabsCommandBase

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandBase, CommandOptionsMixin[Options]):
    def execute_command_helper(self: Command, stunner_dll_object) -> Any:
        status_code_raw, results, results_path = stunner_dll_object.Get_Results(
            self.options.results_definition,
            "",
        )

        return {
            "status_code_raw": status_code_raw,
            "results": results,
            "results_path": results_path,
        }
