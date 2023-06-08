from typing import Any

from ..Backend import UnchainedLabsCommandABC


@UnchainedLabsCommandABC.Decorator_Command(__file__)
class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        return UnchainedLabsCommandABC.ParseResponse(StunnerDLLObject.Close_Tray())
