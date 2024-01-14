from __future__ import annotations

import dataclasses

from plh.driver.UnchainedLabs.backend import UnchainedLabsCommandBase


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandBase):
    def execute_command_helper(
        self: Command,
        stunner_dll_object,
    ) -> dict | Exception:
        status_code_raw, measurement_info = stunner_dll_object.Get_Status("")
        return {
            "status_code_raw": status_code_raw,
            "measurement_info": measurement_info,
        }
