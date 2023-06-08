from dataclasses import dataclass
from typing import Any

from ..Backend import UnchainedLabsCommandABC


@UnchainedLabsCommandABC.Decorator_Command(__file__)
@dataclass
class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        return UnchainedLabsCommandABC.ParseResponse(StunnerDLLObject.Open_Tray())
