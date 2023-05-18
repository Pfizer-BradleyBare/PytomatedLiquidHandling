import subprocess
from typing import Type, TypeVar, cast

from .....Tools.Logger import Logger
from ....Tools.AbstractClasses import BackendABC, CommandABC
from ..HamiltonCommand import (
    HamiltonActionCommandABC,
    HamiltonCommandABC,
    HamiltonStateCommandABC,
)
from .HamiltonServerBackend import HamiltonServerBackendABC

T= TypeVar("T",bound=CommandABC.Response)

class HamiltonBackendABC(BackendABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        LoggerInstance: Logger,
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
            "/ActionServer/",
            767,
        )
        self.StateServer: HamiltonServerBackendABC = HamiltonServerBackendABC(
            UniqueIdentifier + " State Server",
            LoggerInstance,
            "/StateServer/",
            768,
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

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            self.StateServer.WaitForResponseBlocking(CommandInstance)
        else:
            self.ActionServer.WaitForResponseBlocking(CommandInstance)

    def GetResponse(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC, ResponseType: Type[T] 
    ) -> T:
        
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            return self.StateServer.GetResponse(CommandInstance,ResponseType)
        else:
            return self.ActionServer.GetResponse(CommandInstance,ResponseType)
