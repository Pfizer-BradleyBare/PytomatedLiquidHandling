from __future__ import annotations

import dataclasses
from abc import abstractmethod

from plh.driver.tools import CommandBase


@dataclasses.dataclass(kw_only=True)
class UnchainedLabsCommandBase(CommandBase):
    @abstractmethod
    def execute_command_helper(
        self: UnchainedLabsCommandBase,
        stunner_dll_object,
    ) -> dict | Exception:
        ...
