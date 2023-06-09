import os
import subprocess
import threading
from dataclasses import dataclass, field
from typing import Any, TypeVar

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses.Command import CommandABC

from ....Tools.AbstractClasses import SimpleBackendABC
from ..UnchainedLabsCommand import UnchainedLabsCommandABC

T = TypeVar("T", bound=CommandABC.Response)


@dataclass
class StunnerBackend(SimpleBackendABC):
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

    def StunnerRunnerThread(self):
        CommandInstance = self.CommandInstance

        if not isinstance(CommandInstance, UnchainedLabsCommandABC):
            raise Exception("This should never happen")

        self.ResponseInstance = CommandInstance.ParseResponse(
            CommandInstance.ExecuteCommandHelper(self.StunnerDLLObject)
        )

    def StartBackend(self):
        SimpleBackendABC.StartBackend(self)

        ResponseInstance = UnchainedLabsCommandABC.ParseResponse(
            self.StunnerDLLObject.Request_Access()
        )
        CommandInstance = CommandABC("Start Backend")
        SimpleBackendABC.CheckExceptions(CommandInstance, ResponseInstance)

    def StopBackend(self):
        SimpleBackendABC.StopBackend(self)

        ResponseInstance = UnchainedLabsCommandABC.ParseResponse(
            self.StunnerDLLObject.Release_Access()
        )
        CommandInstance = CommandABC("Start Backend")
        SimpleBackendABC.CheckExceptions(CommandInstance, ResponseInstance)

    def ExecuteCommand(self, CommandInstance: UnchainedLabsCommandABC):
        SimpleBackendABC.ExecuteCommand(self, CommandInstance)
        threading.Thread(
            target=StunnerBackend.StunnerRunnerThread, args=(self,)
        ).start()
