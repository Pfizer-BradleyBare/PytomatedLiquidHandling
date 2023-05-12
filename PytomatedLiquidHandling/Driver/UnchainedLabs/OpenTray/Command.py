from typing import Any

from ..Backend import UnchainedLabsCommand


class Command(UnchainedLabsCommand):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        return UnchainedLabsCommand.ParseResponse(StunnerDLLObject.Open_Tray())

    def HandleErrors(self):
        ...
