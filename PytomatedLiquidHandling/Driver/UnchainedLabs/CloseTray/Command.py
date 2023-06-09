from dataclasses import dataclass
from typing import Any, cast

from ..Backend import UnchainedLabsCommandABC


@dataclass
class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        return StunnerDLLObject.Close_Tray()
