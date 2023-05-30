from .BaseTransportDevice import TransportOptions
from .BaseTransportDevice import TransportableLabwareTracker, TransportDevice
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Transport import IPG as IPGDriver


class InternalPlateGripper(TransportDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        TransportDevice.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            TransportableLabwareTrackerInstance,
        )

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
            self.TransportableLabwareTrackerInstance.GetObjectByName(
                SourceLayoutItem.LabwareInstance.GetUniqueIdentifier()
            )
        )

        try:
            CommandInstance = IPGDriver.GetPlate.Command(
                OptionsInstance=IPGDriver.GetPlate.Options(
                    PlateSequence=SourceLayoutItem.Sequence,
                    GripWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
                    - SourceTransportableLabware.TransportParametersInstance.CloseOffset,
                    OpenWidth=SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
                    + SourceTransportableLabware.TransportParametersInstance.OpenOffset,
                    GripHeight=SourceTransportableLabware.TransportParametersInstance.PickupHeight,
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            self.GetBackend().GetResponse(CommandInstance, CommandInstance.Response)

        except:
            ...

        try:
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            self.GetBackend().GetResponse(CommandInstance, CommandInstance.Response)

        except:
            ...

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
