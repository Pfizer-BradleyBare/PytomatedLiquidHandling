from abc import abstractmethod

import dataclasses

from ....Tools.BaseClasses import CommandABC


@dataclasses.dataclass(kw_only=True)
class UnchainedLabsCommandABC(CommandABC):
    @abstractmethod
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        ...
