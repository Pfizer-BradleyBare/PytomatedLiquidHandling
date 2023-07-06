from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Transport import IPG as IPGDriver
from .BaseTransportDevice import TransportDevice, TransportOptions


@dataclass
class HamiltonInternalPlateGripper(TransportDevice):
    BackendInstance: HamiltonBackendABC

    def Initialize(
        self,
    ):
        ...

    def Deinitialize(
        self,
    ):
        ...

    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        self._CheckIsValid(TransportOptionsInstance)

        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

        SourceTransportableLabware = (
            self.SupportedLabwareTrackerInstance.GetObjectByName(
                SourceLayoutItem.LabwareInstance.UniqueIdentifier
            )
        )

        CommandInstance = IPGDriver.GetPlate.Command(
            OptionsInstance=IPGDriver.GetPlate.Options(
                PlateSequence=SourceLayoutItem.Sequence,
                GripWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
                - SourceTransportableLabware.TransportOffsetsInstance.Close,
                OpenWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
                + SourceTransportableLabware.TransportOffsetsInstance.Open,
                GripHeight=SourceTransportableLabware.TransportOffsetsInstance.Height,
                GripMode=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "GripMode"
                ],
                Movement=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "Movement"
                ],
                RetractDistance=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "RetractDistance"
                ],
                LiftupHeight=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "LiftupHeight"
                ],
                LabwareOrientation=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "LabwareOrientation"
                ],
                InverseGrip=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "InverseGrip"
                ],
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, IPGDriver.GetPlate.Response)

        CommandInstance = IPGDriver.PlacePlate.Command(
            OptionsInstance=IPGDriver.PlacePlate.Options(
                PlateSequence=DestinationLayoutItem.Sequence,
                Movement=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "Movement"
                ],
                RetractDistance=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "RetractDistance"
                ],
                LiftupHeight=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "LiftupHeight"
                ],
                LabwareOrientation=SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig[
                    "LabwareOrientation"
                ],
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, IPGDriver.PlacePlate.Response)

    def GetGetConfigKeys(self) -> list[str]:
        return [
            "GripMode",
            "Movement",
            "RetractDistance",
            "LiftupHeight",
            "LabwareOrientation",
            "InverseGrip",
        ]

    def GetPlaceConfigKeys(self) -> list[str]:
        return [
            "Movement",
            "RetractDistance",
            "LiftupHeight",
            "LabwareOrientation",
        ]
