from dataclasses import dataclass
from typing import cast

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Transport import COREGripper as COREGripperDriver
from .Base import DeckLocationTransportConfig, TransportDeviceABC, TransportOptions


@dataclass
class HamiltonCOREGripper(TransportDeviceABC):
    BackendInstance: HamiltonBackendABC
    GripperToolSequence: str

    class GetConfig(DeckLocationTransportConfig.TransportConfigABC):
        def __init__(self, Config: dict):
            ...

        def _ComparisonKeys(self) -> list[str]:
            return []

    class PlaceConfig(DeckLocationTransportConfig.TransportConfigABC):
        def __init__(self, Config: dict):
            self.CheckPlateExists: COREGripperDriver.PlacePlate.Options.YesNoOptions = (
                COREGripperDriver.PlacePlate.Options.YesNoOptions(
                    Config["CheckPlateExists"]
                )
            )

        def _ComparisonKeys(self) -> list[str]:
            return ["CheckPlateExists"]

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        self._CheckIsValid(TransportOptionsInstance)

        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

        SourceTransportableLabware = (
            self.SupportedLabwareTrackerInstance.GetObjectByName(
                SourceLayoutItem.LabwareInstance.UniqueIdentifier
            )
        )

        GetPlateOptionsInstance = COREGripperDriver.GetPlate.Options(
            GripperSequence=self.GripperToolSequence,
            PlateSequence=SourceLayoutItem.Sequence,
            GripWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
            - SourceTransportableLabware.TransportOffsetsInstance.Close,
            OpenWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
            + SourceTransportableLabware.TransportOffsetsInstance.Open,
            GripHeight=SourceTransportableLabware.TransportOffsetsInstance.Height,
        )

        CommandInstance = COREGripperDriver.GetPlate.Command(
            OptionsInstance=GetPlateOptionsInstance,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(
            CommandInstance, COREGripperDriver.GetPlate.Response
        )

        PlaceConfigInstance = (
            self.DeckLocationTransportConfigTrackerInstance.GetObjectByName(
                DestinationLayoutItem.DeckLocationInstance.UniqueIdentifier
            ).PlaceConfig
        )

        if not isinstance(PlaceConfigInstance, self.PlaceConfig):
            raise Exception("This should never happen")

        CommandInstance = COREGripperDriver.PlacePlate.Command(
            OptionsInstance=COREGripperDriver.PlacePlate.Options(
                PlateSequence=DestinationLayoutItem.Sequence,
                CheckPlateExists=PlaceConfigInstance.CheckPlateExists,
                EjectTool=COREGripperDriver.PlacePlate.Options.YesNoOptions(
                    int(self._LastTransportFlag)
                ),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(
            CommandInstance, COREGripperDriver.PlacePlate.Response
        )
