from dataclasses import dataclass
from typing import Any, cast

from ..Backend import UnchainedLabsCommandABC


@dataclass
class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(
        self, StunnerDLLObject
    ) -> UnchainedLabsCommandABC.Response:
        return cast(
            UnchainedLabsCommandABC.Response,
            UnchainedLabsCommandABC.ParseResponse(StunnerDLLObject.Close_Tray()),
        )
