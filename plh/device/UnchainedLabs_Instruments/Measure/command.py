from __future__ import annotations

import dataclasses

from plh.device.tools import CommandOptionsMixin
from plh.device.UnchainedLabs_Instruments.backend import UnchainedLabsCommandBase

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandBase, CommandOptionsMixin[Options]):
    def execute_command_helper(
        self: Command,
        stunner_dll_object,
    ) -> dict | Exception:
        from System import String  # type:ignore

        plate_id = self.options.plate_id
        if plate_id is None:
            status_code_raw, plate_id = stunner_dll_object.Measure()

        else:
            status_code_raw = stunner_dll_object.Measure.__overloads__[String](plate_id)

        # Pythonnet allows us to select the specific overload. In this case there are two:
        # 1. Input string
        # 2. Output string
        # By default the output string is selected. The overload above selects the input string overload.

        return {"status_code_raw": status_code_raw, "plate_id": plate_id}
