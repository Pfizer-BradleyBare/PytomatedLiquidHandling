from dataclasses import dataclass
from typing import Any

from ..Backend import UnchainedLabsCommandABC


@dataclass(kw_only=True)
class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        return StunnerDLLObject.Close_Tray()
