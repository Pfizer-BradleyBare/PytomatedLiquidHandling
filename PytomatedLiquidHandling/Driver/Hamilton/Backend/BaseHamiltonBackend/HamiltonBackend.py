import os
import shutil
import subprocess
from platform import platform
from typing import Any, Type, TypeVar

from pydantic import PrivateAttr

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
    SimulationOn: bool = True
    _ActionServer: HamiltonServerBackendABC = PrivateAttr()
    _StateServer: HamiltonServerBackendABC = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        BackendABC.model_post_init(self, __context)
        self._ActionServer: HamiltonServerBackendABC = HamiltonServerBackendABC(
            Identifier=str(self.Identifier) + " Action Server",
            PathPrefix="/ActionServer/",
            Port=767,
        )
        self._StateServer: HamiltonServerBackendABC = HamiltonServerBackendABC(
            Identifier=str(self.Identifier) + " State Server",
            PathPrefix="/StateServer/",
            Port=768,
        )

    def StartBackend(self):
        if "windows" not in platform().lower():
            raise RuntimeError(
                "Hamilton backend is only supported on Windows PCs. Sorry!"
            )

        BackendABC.StartBackend(self)

        HamiltonDeckLayoutBasePath = "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Driver\\Hamilton\\Backend\\BaseHamiltonBackend\\Layout\\Layout.lay"
        os.makedirs(
            os.path.dirname(HamiltonDeckLayoutBasePath), mode=777, exist_ok=True
        )

        if not os.path.exists(self.DeckLayoutPath):
            raise RuntimeError(
                "Layout File not found. Ensure the layout file exists in this location: "
                + self.DeckLayoutPath
            )
        shutil.copyfile(self.DeckLayoutPath, HamiltonDeckLayoutBasePath)
        shutil.copyfile(
            self.DeckLayoutPath.replace(".lay", ".res"),
            HamiltonDeckLayoutBasePath.replace(".lay", ".res"),
        )
        # Move layout file into temp folder. Layouts are comprised of 2 files: .lay, and .res

        SimulationConfigFile = (
            "C:\\Program Files (x86)\\HAMILTON\\Config\\HxServices.cfg"
        )

        process = subprocess.Popen(
            [
                "C:\\Program Files (x86)\\HAMILTON\\Bin\\HxCfgFilConverter.exe",
                "/t",
                SimulationConfigFile,
            ],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        process.communicate()
        # Taken from PyVenus by SNIPR Biome. Thank you!!

        File = open(SimulationConfigFile, "r")
        Contents = (
            File.read()
            .replace(
                'SimulationOn, "1",',
                'SimulationOn, "' + str(int(self.SimulationOn)) + '",',
            )
            .replace(
                'SimulationOn, "0",',
                'SimulationOn, "' + str(int(self.SimulationOn)) + '",',
            )
        )
        File.close()
        File = open(SimulationConfigFile, "w")
        File.write(Contents)
        File.close()
        # Turn on or off simulation mode

        subprocess.Popen(
            ["C:\\Program Files (x86)\\HAMILTON\\Bin\\HxRun.exe", "-t", self.MethodPath]
        )

        self._ActionServer.StartBackend()
        self._StateServer.StartBackend()

    def StopBackend(self):
        BackendABC.StopBackend(self)

        class AbortCommand(HamiltonActionCommandABC):
            ...

        Command = AbortCommand(CustomErrorHandling=True)
        self._ActionServer._Command = Command
        self._ActionServer.WaitForResponseBlocking(Command)

        self._ActionServer.StopBackend()
        self._StateServer.StopBackend()

    def ExecuteCommand(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC
    ):
        BackendABC.ExecuteCommand(self, CommandInstance)
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            self._StateServer.ExecuteCommand(CommandInstance)
        else:
            self._ActionServer.ExecuteCommand(CommandInstance)

    def GetCommandStatus(
        self, CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC
    ) -> ResponseABC:
        BackendABC.GetCommandStatus(self, CommandInstance)
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            return self._StateServer.GetCommandStatus(CommandInstance)
        else:
            return self._ActionServer.GetCommandStatus(CommandInstance)

    def WaitForResponseBlocking(self, CommandInstance: CommandABC):
        BackendABC.WaitForResponseBlocking(self, CommandInstance)
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            self._StateServer.WaitForResponseBlocking(CommandInstance)
        else:
            self._ActionServer.WaitForResponseBlocking(CommandInstance)

    def GetResponse(
        self,
        CommandInstance: HamiltonActionCommandABC | HamiltonStateCommandABC,
        ResponseType: Type[HamiltonResponseABCType],
    ) -> HamiltonResponseABCType:
        BackendABC.GetResponse(self, CommandInstance, ResponseType)
        if isinstance(CommandInstance, HamiltonStateCommandABC):
            return self._StateServer.GetResponse(CommandInstance, ResponseType)

        else:
            return self._ActionServer.GetResponse(CommandInstance, ResponseType)
