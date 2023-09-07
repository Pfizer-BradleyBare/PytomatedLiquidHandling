from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Transport import IPG as IPGDriver
from .Base import DeckLocationTransportConfig, TransportDeviceABC, TransportOptions


@dataclass
class HamiltonInternalPlateGripper(TransportDeviceABC):
    BackendInstance: HamiltonBackendABC

    class GetConfig(DeckLocationTransportConfig.TransportConfigABC):
        def __init__(self, Config: dict):
            self.GripMode: IPGDriver.GetPlate.Options.GripModeOptions = (
                IPGDriver.GetPlate.Options.GripModeOptions[Config["GripMode"]]
            )
            self.Movement: IPGDriver.GetPlate.Options.MovementOptions = (
                IPGDriver.GetPlate.Options.MovementOptions[Config["Movement"]]
            )
            self.RetractDistance: float = Config["RetractDistance"]
            self.LiftupHeight: float = Config["LiftupHeight"]
            self.LabwareOrientation: IPGDriver.GetPlate.Options.LabwareOrientationOptions = IPGDriver.GetPlate.Options.LabwareOrientationOptions[
                Config["LabwareOrientation"]
            ]
            self.InverseGrip: IPGDriver.GetPlate.Options.YesNoOptions = (
                IPGDriver.GetPlate.Options.YesNoOptions(Config["InverseGrip"])
            )

        def _ComparisonKeys(self) -> list[str]:
            return [
                "GripMode",
                "Movement",
                "LabwareOrientation",
                "InverseGrip",
            ]

    class PlaceConfig(DeckLocationTransportConfig.TransportConfigABC):
        def __init__(self, Config: dict):
            self.Movement: IPGDriver.PlacePlate.Options.MovementOptions = (
                IPGDriver.PlacePlate.Options.MovementOptions[Config["Movement"]]
            )
            self.RetractDistance: float = Config["RetractDistance"]
            self.LiftupHeight: float = Config["LiftupHeight"]
            self.LabwareOrientation: IPGDriver.PlacePlate.Options.LabwareOrientationOptions = IPGDriver.PlacePlate.Options.LabwareOrientationOptions[
                Config["LabwareOrientation"]
            ]

        def _ComparisonKeys(self) -> list[str]:
            return [
                "Movement",
                "LabwareOrientation",
            ]

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        self._CheckIsValid(TransportOptionsInstance)

        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

        SourceTransportableLabware = (
            self.SupportedLabwareTrackerInstance.GetObjectByName(
                SourceLayoutItem.LabwareInstance.UniqueIdentifier
            )
        )

        GetConfigInstance = (
            self.DeckLocationTransportConfigTrackerInstance.GetObjectByName(
                SourceLayoutItem.DeckLocationInstance.UniqueIdentifier
            ).GetConfig
        )

        if not isinstance(GetConfigInstance, self.GetConfig):
            raise Exception("This should never happen")

        CommandInstance = IPGDriver.GetPlate.Command(
            OptionsInstance=IPGDriver.GetPlate.Options(
                PlateSequence=SourceLayoutItem.Sequence,
                GripWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
                - SourceTransportableLabware.TransportOffsetsInstance.Close,
                OpenWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
                + SourceTransportableLabware.TransportOffsetsInstance.Open,
                GripHeight=SourceTransportableLabware.TransportOffsetsInstance.Height,
                GripMode=GetConfigInstance.GripMode,
                Movement=GetConfigInstance.Movement,
                RetractDistance=GetConfigInstance.RetractDistance,
                LiftupHeight=GetConfigInstance.LiftupHeight,
                LabwareOrientation=GetConfigInstance.LabwareOrientation,
                InverseGrip=GetConfigInstance.InverseGrip,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, IPGDriver.GetPlate.Response)

        PlaceConfigInstance = (
            self.DeckLocationTransportConfigTrackerInstance.GetObjectByName(
                DestinationLayoutItem.DeckLocationInstance.UniqueIdentifier
            ).PlaceConfig
        )

        if not isinstance(PlaceConfigInstance, self.PlaceConfig):
            raise Exception("This should never happen")

        CommandInstance = IPGDriver.PlacePlate.Command(
            OptionsInstance=IPGDriver.PlacePlate.Options(
                PlateSequence=DestinationLayoutItem.Sequence,
                Movement=PlaceConfigInstance.Movement,
                RetractDistance=PlaceConfigInstance.RetractDistance,
                LiftupHeight=PlaceConfigInstance.LiftupHeight,
                LabwareOrientation=PlaceConfigInstance.LabwareOrientation,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, IPGDriver.PlacePlate.Response)
