from typing import Any

from ..Backend import UnchainedLabsOptionsCommand


class Command(UnchainedLabsOptionsCommand):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        return StunnerDLLObject.Open_Tray()

    def HandleErrors(self):
        ...
