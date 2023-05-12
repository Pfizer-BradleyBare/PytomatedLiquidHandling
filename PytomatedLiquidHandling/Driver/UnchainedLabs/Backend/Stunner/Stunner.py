import os
import subprocess
from typing import Any

import clr

from ....Tools.AbstractBackend import BackendABC


class Stunner(BackendABC):
    def __init__(self, InstrumentIPAddress: str, InstrumentPort: int):

        self.InstrumentIPAddress: str = InstrumentIPAddress
        self.InstrumentPort: int = InstrumentPort
        self.CurrentExperimentDefinition: dict[str, Any] | None = None

        BasePath = os.path.dirname(__file__)

        Args = (
            os.path.join(BasePath, "streams.exe")
            + ' -d "'
            + os.path.join(BasePath, "Stunner.dll")
            + '"'
        )
        subprocess.call(Args)

        clr.AddReference(os.path.join(BasePath, "Stunner.dll"))  # type: ignore
        from UnchainedLabs_Instruments import Stunner  # type: ignore

        self.StunnerDLLObject = Stunner(InstrumentIPAddress, InstrumentPort)

    def StartBackend(self):
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
        StatusCode = self.StunnerDLLObject.Release_Access()

        if int(StatusCode) == 0:
            return

        elif int(StatusCode) == -1:
            raise Exception(
                "You need to start the backend first. You do not have access"
            )

        elif int(StatusCode) == 0:
            raise Exception(
                "Backend was not reachable over the network. Is the Stunner turn on and configured for API mode?"
            )

    def GetRawStatus(self) -> int:
        return self.StunnerDLLObject.Get_Status()

    def SendCommand(self, CommandParams: dict[str, Any]):
        ...

    # No def because this will never be used in this backend

    def ResponseReady(self) -> bool:
        StatusCode = self.GetRawStatus()

        if StatusCode == 0:
            return True
        else:
            return False

    def GetResponse(self) -> dict[str, list[Any]]:
        return super().GetResponse()
