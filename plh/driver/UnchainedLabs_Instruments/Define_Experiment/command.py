from __future__ import annotations

import dataclasses
from typing import Any

from plh.driver.tools import CommandOptionsMixin
from plh.driver.UnchainedLabs_Instruments.backend import UnchainedLabsCommandBase

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandBase, CommandOptionsMixin[Options]):
    def execute_command_helper(self: Command, stunner_dll_object) -> Any:
        status_code_raw, defined_plate_ids = stunner_dll_object.Define_Experiment(
            self.options.experiment_definition,
            self.options.sample_definition,
        )

        return {
            "status_code_raw": status_code_raw,
            "defined_plate_ids": defined_plate_ids,
        }
