import subprocess

from .....Tools.Logger import Logger
from ....Tools.AbstractClasses import BackendABC
from ..HamiltonCommand import (
    HamiltonActionCommandABC,
    HamiltonCommandABC,
    HamiltonStateCommandABC,
)
from .HamiltonServerBackend import HamiltonServerBackendABC


class HamiltonBackendABC(BackendABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        LoggerInstance: Logger,
        PathPrefix: str = "/",
        Port: int = 8080,
        MethodPath: str = "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\test.hsl",
    ):
        BackendABC.__init__(
            self,
            UniqueIdentifier,
            LoggerInstance,
        )

        self.ActionServer: HamiltonServerBackendABC = HamiltonServerBackendABC(
            UniqueIdentifier + " Action Server",
            LoggerInstance,
            PathPrefix + "ActionServer/",
            Port,
        )
        self.StateServer: HamiltonServerBackendABC = HamiltonServerBackendABC(
            UniqueIdentifier + " State Server",
            LoggerInstance,
            PathPrefix + "StateServer/",
            Port + 1,
        )

        self.MethodPath: str = MethodPath

    def StartBackend(self):
        subprocess.Popen(
            ["C:\\Program Files (x86)\\HAMILTON\\Bin\\HxRun.exe", "-t", self.MethodPath]
        )

        self.ActionServer.StartBackend()
        self.StateServer.StartBackend()

    def StopBackend(self):
        self.ActionServer.StopBackend()
        self.StateServer.StopBackend()

    def ExecuteCommand(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC
    ):

        if isinstance(CommandInstance, HamiltonStateCommandABC):
            self.StateServer.ExecuteCommand(CommandInstance)
        else:
            self.ActionServer.ExecuteCommand(CommandInstance)

    def GetStatus(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC
    ) -> HamiltonCommandABC.Response:

        if isinstance(CommandInstance, HamiltonStateCommandABC):
            return self.StateServer.GetStatus(CommandInstance)
        else:
            return self.ActionServer.GetStatus(CommandInstance)

    def GetResponse(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC
    ) -> HamiltonActionCommandABC.Response | HamiltonStateCommandABC.Response:

        if isinstance(CommandInstance, HamiltonStateCommandABC):
            return self.StateServer.GetResponse(CommandInstance)
        else:
            return self.ActionServer.GetResponse(CommandInstance)
