from typing import Any

from ..Backend import UnchainedLabsCommandABC


class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        return StunnerDLLObject.Open_Tray()

    def ParseResponseRaiseExceptions(
        self, ResponseInstance: UnchainedLabsCommandABC.Response
    ):
        ...
