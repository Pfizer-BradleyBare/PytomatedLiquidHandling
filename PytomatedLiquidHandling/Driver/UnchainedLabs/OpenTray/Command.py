from typing import Any

from ..Backend import UnchainedLabsCommandABC


class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        return UnchainedLabsCommandABC.ParseResponse(StunnerDLLObject.Open_Tray())

    def HandleErrors(self):
        ...