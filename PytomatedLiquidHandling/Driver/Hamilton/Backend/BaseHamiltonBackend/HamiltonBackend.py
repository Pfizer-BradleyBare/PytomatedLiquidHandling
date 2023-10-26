import os
import shutil
import subprocess
from pydantic import PrivateAttr
from typing import Type, TypeVar

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import (
    BackendABC,
    CommandABC,
    ResponseABC,
)

from ..HamiltonCommand import HamiltonActionCommandABC, HamiltonStateCommandABC
from ..HamiltonResponse import HamiltonResponseABC
from .HamiltonServerBackend import HamiltonServerBackendABC

HamiltonResponseABCType = TypeVar("HamiltonResponseABCType", bound=HamiltonResponseABC)


class HamiltonBackendABC(BackendABC):
    MethodPath: str
    DeckLayoutPath: str
    _ActionServer: HamiltonServerBackendABC = PrivateAttr()
    _StateServer: HamiltonServerBackendABC = PrivateAttr()

    def __post_init__(self):
        self.ActionServer: HamiltonServerBackendABC = HamiltonServerBackendABC(
            Identifier=str(self.Identifier) + " Action Server",
            PathPrefix="/ActionServer/",
            Port=767,
        )
        self.StateServer: HamiltonServerBackendABC = HamiltonServerBackendABC(
            Identifier=str(self.Identifier) + " State Server",
            PathPrefix="/StateServer/",
            Port=768,
        )

        # self._Exceptions = [
        #    HamiltonExceptions.UnhandledException,
        #    HamiltonExceptions.NoOptionsInTracker,
        # ]

    def StartBackend(self):
        BackendABC.StartBackend(self)

        HamiltonDeckLayoutBasePath = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\BaseHamiltonBackend\\Hamilton\\Layout\\Temp\\ExampleLayout.lay"
        os.makedirs(
            os.path.dirname(HamiltonDeckLayoutBasePath), mode=777, exist_ok=True
        )

        if not os.path.exists(self.DeckLayoutPath):
            raise Exception(
                "Layout File not found. Ensure the layout file exists in this location: "
                + self.DeckLayoutPath
            )
        shutil.copyfile(self.DeckLayoutPath, HamiltonDeckLayoutBasePath)
        shutil.copyfile(
            self.DeckLayoutPath.replace(".lay", ".res"),
            HamiltonDeckLayoutBasePath.replace(".lay", ".res"),
        )
        # Move layout file into temp folder. Layouts are comprised of 2 files: .lay, and .res

        subprocess.Popen(
            ["C:\\Program Files (x86)\\HAMILTON\\Bin\\HxRun.exe", "-t", self.MethodPath]
        )

        self.ActionServer.StartBackend()
        self.StateServer.StartBackend()

    def StopBackend(self):
        BackendABC.StopBackend(self)
        self.ActionServer.StopBackend()
        self.StateServer.StopBackend()

    def ExecuteCommand(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC
    ):
        BackendABC.ExecuteCommand(self, CommandInstance)
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            self.StateServer.ExecuteCommand(CommandInstance)
        else:
            self.ActionServer.ExecuteCommand(CommandInstance)

    def GetCommandStatus(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC
    ) -> ResponseABC:
        BackendABC.GetCommandStatus(self, CommandInstance)
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            return self.StateServer.GetCommandStatus(CommandInstance)
        else:
            return self.ActionServer.GetCommandStatus(CommandInstance)

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        BackendABC.WaitForResponseBlocking(self, CommandInstance)
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            self.StateServer.WaitForResponseBlocking(CommandInstance)
        else:
            self.ActionServer.WaitForResponseBlocking(CommandInstance)

    def GetResponse(
        self,
        CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC,
        ResponseType: Type[HamiltonResponseABCType],
    ) -> HamiltonResponseABCType:
        BackendABC.GetResponse(self, CommandInstance, ResponseType)
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            return ResponseType(
                self.StateServer.GetResponse(CommandInstance, ResponseType).Properties
            )
        else:
            return ResponseType(
                self.ActionServer.GetResponse(CommandInstance, ResponseType).Properties
            )
