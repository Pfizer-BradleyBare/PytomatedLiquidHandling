from __future__ import annotations

import dataclasses

from plh.device.UnchainedLabs_Instruments.backend import UnchainedLabsCommandBase


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandBase):
    def execute_command_helper(
        self: Command,
        stunner_dll_object,
    ) -> dict | Exception:
        return {
            "status_code_raw": 0,
            "internal_error_description": stunner_dll_object.GetLastInternalError(),
        }
