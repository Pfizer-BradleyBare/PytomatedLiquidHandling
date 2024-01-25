from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("PytomatedLiquidHandling")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))


hamilton_backend = hal.backend.devices["Hamilton"]

hamilton_backend.start()

tip = hal.tip.devices["1000uL FTR"]

tip.initialize()

plate = hal.layout_item.devices["Carrier42_Pos1_Biorad200uLPCRPlate"]

pipette = hal.pipette.devices["Pipette"]

pipette.initialize()

pipette_tip = pipette.supported_tips[0]

pipette._pickup(
    [
        hal.pipette._PickupOptions(ChannelNumber=1, PipetteTip=pipette_tip),
        hal.pipette._PickupOptions(ChannelNumber=2, PipetteTip=pipette_tip),
        hal.pipette._PickupOptions(ChannelNumber=3, PipetteTip=pipette_tip),
        hal.pipette._PickupOptions(ChannelNumber=4, PipetteTip=pipette_tip),
        hal.pipette._PickupOptions(ChannelNumber=5, PipetteTip=pipette_tip),
        hal.pipette._PickupOptions(ChannelNumber=6, PipetteTip=pipette_tip),
        hal.pipette._PickupOptions(ChannelNumber=7, PipetteTip=pipette_tip),
        hal.pipette._PickupOptions(ChannelNumber=8, PipetteTip=pipette_tip),
    ],
)

input("enter")

pipette._aspirate(
    [
        hal.pipette._AspirateDispenseOptions(
            ChannelNumber=1,
            LayoutItem=plate,
            PositionID="A1",
            WellVolume=10,
            MixCycles=0,
            MixVolume=0,
            LiquidClass="HighVolume_Water_DispenseSurface_Empty",
            Volume=30,
        ),
        hal.pipette._AspirateDispenseOptions(
            ChannelNumber=2,
            LayoutItem=plate,
            PositionID="B1",
            WellVolume=50,
            MixCycles=0,
            MixVolume=0,
            LiquidClass="HighVolume_Water_DispenseSurface_Empty",
            Volume=30,
        ),
        hal.pipette._AspirateDispenseOptions(
            ChannelNumber=3,
            LayoutItem=plate,
            PositionID="C1",
            WellVolume=100,
            MixCycles=0,
            MixVolume=0,
            LiquidClass="HighVolume_Water_DispenseSurface_Empty",
            Volume=30,
        ),
        hal.pipette._AspirateDispenseOptions(
            ChannelNumber=4,
            LayoutItem=plate,
            PositionID="D1",
            WellVolume=150,
            MixCycles=5,
            MixVolume=100,
            LiquidClass="HighVolume_Water_DispenseSurface_Empty",
            Volume=30,
        ),
    ],
)

input("enter")

pipette._eject(
    [
        hal.pipette._EjectOptions(
            ChannelNumber=1,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID="1",
        ),
        hal.pipette._EjectOptions(
            ChannelNumber=2,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID="2",
        ),
        hal.pipette._EjectOptions(
            ChannelNumber=3,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID="3",
        ),
        hal.pipette._EjectOptions(
            ChannelNumber=4,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID="4",
        ),
        hal.pipette._EjectOptions(
            ChannelNumber=5,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID="5",
        ),
        hal.pipette._EjectOptions(
            ChannelNumber=6,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID="6",
        ),
        hal.pipette._EjectOptions(
            ChannelNumber=7,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID="7",
        ),
        hal.pipette._EjectOptions(
            ChannelNumber=8,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID="8",
        ),
    ],
)

pipette.deinitialize()

tip.deinitialize()

hamilton_backend.stop()
