import os
import subprocess
from dataclasses import dataclass, field
from typing import Any, Type, TypeVar

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses.Command import CommandABC

from ....Tools.AbstractClasses import BackendABC
from ..UnchainedLabsCommand import UnchainedLabsCommandABC

T = TypeVar("T", bound=CommandABC.Response)


@dataclass
class StunnerBackend(BackendABC):
    InstrumentIPAddress: str
    InstrumentPort: int
    StunnerDLLObject: Any = field(init=False)

    def __post_init__(self):
        BasePath = os.path.dirname(__file__)

        Args = (
            os.path.join(BasePath, "streams.exe")
            + ' -d "'
            + os.path.join(BasePath, "Stunner.dll")
            + '"'
        )
        subprocess.call(Args)
        # The stunner API access uses a .DLL library. This step cleans the .dll.
        # Microsoft will not let you load a .dll without cleaning it first.

        import clr

        clr.AddReference(os.path.join(BasePath, "Stunner.dll"))  # type: ignore
        from UnchainedLabs_Instruments import Stunner  # type: ignore

        # The stunner API access uses a .DLL library. This step loads the .dll as a module.

        self.StunnerDLLObject = Stunner(self.InstrumentIPAddress, self.InstrumentPort)
        # The stunner API access uses a .DLL library. This step creates the stunner class present in the .dll.

    def StartBackend(self):
        BackendABC.StartBackend(self)
        StatusCode = self.StunnerDLLObject.Request_Access()

        if int(StatusCode) == 0:
            return

        elif int(StatusCode) == 1:
            raise Exception("You already have access. Do not start the backend twice.")

        elif int(StatusCode) == -1:
            raise Exception(
                "Another device currently has access. Please try again later."
            )

        elif int(StatusCode) == 0:
            raise Exception(
                "Backend was not reachable over the network. Is the Stunner turn on and configured for API mode?"
            )

    def StopBackend(self):
        BackendABC.StopBackend(self)
        StatusCode = self.StunnerDLLObject.Release_Access()

        if int(StatusCode) == 0:
            return

        elif int(StatusCode) == -1:
            raise Exception(
                "You need to start the backend first. You do not have access"
            )

        elif int(StatusCode) == 0:
            raise Exception(
                "Backend was not reachable over the network. Is the Stunner turned on and configured for API mode?"
            )
