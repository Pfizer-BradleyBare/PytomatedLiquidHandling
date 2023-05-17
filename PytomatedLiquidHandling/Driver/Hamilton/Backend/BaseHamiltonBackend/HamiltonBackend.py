import os
import subprocess
import time

from flask import request

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses.Command import CommandABC

from .....Tools.Logger import Logger
from ....Tools.AbstractClasses import BackendABC
from ..HamiltonCommand import HamiltonActionCommandABC, HamiltonStateCommandABC
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
            Port,
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
        return BackendABC.ExecuteCommand(self, CommandInstance)

    def GetResponse(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC
    ) -> HamiltonActionCommandABC.Response | HamiltonStateCommandABC.Response:
        return super().GetResponse(CommandInstance)
