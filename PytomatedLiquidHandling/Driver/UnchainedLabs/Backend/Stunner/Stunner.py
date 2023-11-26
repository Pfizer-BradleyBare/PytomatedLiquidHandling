import os
import subprocess
import threading
from pydantic import PrivateAttr
from typing import Any

from ....Tools.AbstractClasses import SimpleBackendABC
from ..UnchainedLabsCommand import UnchainedLabsCommandABC
from ..UnchainedLabsResponse import UnchainedLabsResponseABC


class StunnerBackend(SimpleBackendABC):
    InstrumentIPAddress: str
    InstrumentPort: int
    _StunnerDLLObject: Any = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        SimpleBackendABC.model_post_init(self, __context)
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
        # Namespace is "UnchainedLabs_Instruments" and class is Stunner (This is a C# dll)

        self._StunnerDLLObject = Stunner(self.InstrumentIPAddress, self.InstrumentPort)
        # The stunner API access uses a .DLL library. This step creates the stunner class present in the .dll.

    def StartBackend(self):
        SimpleBackendABC.StartBackend(self)

        UnchainedLabsResponseABC(StatusCode=self._StunnerDLLObject.Request_Access())

    def StopBackend(self):
        SimpleBackendABC.StopBackend(self)

        UnchainedLabsResponseABC(StatusCode=self._StunnerDLLObject.Release_Access())

    def ExecuteCommand(self, Command: UnchainedLabsCommandABC):
        SimpleBackendABC.ExecuteCommand(self, Command)

        self._Response = Command._ExecuteCommandHelper(self._StunnerDLLObject)
