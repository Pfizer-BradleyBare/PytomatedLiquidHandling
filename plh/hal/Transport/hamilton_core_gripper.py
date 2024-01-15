from dataclasses import field
from typing import cast

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uLCOREGrip
from plh.hal import deck_location, layout_item

from .transport_base import TransportBase


@dataclasses.dataclass(kw_only=True)
class HamiltonCOREGripper(TransportBase):
    backend: HamiltonBackendBase
    gripper_labware_id: str

    @dataclasses.dataclass(kw_only=True)
    class PickupOptions(TransportBase.PickupOptions):
        """Options to pick up labware from deck location"""

    @dataclasses.dataclass(kw_only=True)
    class DropoffOptions(TransportBase.DropoffOptions):
        """Options to drop off labware to deck location"""

        CheckPlateExists: Channel1000uLCOREGrip.PlacePlate.Options.YesNoOptions = field(
            compare=False,
        )

    def Transport(
        self,
        SourceLayoutItem: layout_item.LayoutItemBase,
        DestinationLayoutItem: layout_item.LayoutItemBase,
    ):
        if SourceLayoutItem.deck_location == DestinationLayoutItem.deck_location:
            return

        CompatibleConfigs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                SourceLayoutItem.deck_location,
                DestinationLayoutItem.deck_location,
            )[0]
        )

        Labware = SourceLayoutItem.labware

        GetPlateOptionsInstance = Channel1000uLCOREGrip.GetPlate.Options(
            GripperLabwareID=self.gripper_labware_id,
            PlateLabwareID=SourceLayoutItem.labware_id,
            GripWidth=Labware.Dimensions.YLength - Labware.TransportOffsets.Close,
            OpenWidth=Labware.Dimensions.YLength + Labware.TransportOffsets.Open,
            GripHeight=Labware.TransportOffsets.Top,
        )

        CommandInstance = Channel1000uLCOREGrip.GetPlate.Command(
            Options=GetPlateOptionsInstance,
            BackendErrorHandling=self.BackendErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(
            CommandInstance,
            Channel1000uLCOREGrip.GetPlate.Response,
        )

        DropoffOptions = cast(
            HamiltonCOREGripper.DropoffOptions,
            CompatibleConfigs[1].DropoffOptions,
        )

        CommandInstance = Channel1000uLCOREGrip.PlacePlate.Command(
            Options=Channel1000uLCOREGrip.PlacePlate.Options(
                LabwareID=DestinationLayoutItem.LabwareID,
                CheckPlateExists=DropoffOptions.CheckPlateExists,
                EjectTool=Channel1000uLCOREGrip.PlacePlate.Options.YesNoOptions(
                    int(self._LastTransportFlag),
                ),
            ),
            BackendErrorHandling=self.BackendErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self.Backend.GetResponse(
            CommandInstance,
            Channel1000uLCOREGrip.PlacePlate.Response,
        )

    def TransportTime(
        self,
        SourceLayoutItem: layout_item.LayoutItemBase,
        DestinationLayoutItem: layout_item.LayoutItemBase,
    ) -> float:
        return 0
