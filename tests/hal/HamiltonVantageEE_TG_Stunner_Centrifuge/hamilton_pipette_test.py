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

position_ids = ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"]
well_volumes = [5, 25, 50, 100, 150, 200, 300, 400]
volumes = [5, 25, 50, 100, 150, 200, 300, 400]
mix_cycles = [0, 0, 0, 5, 0, 0, 0, 5]
mix_volumes = [0, 0, 0, 100, 0, 0, 0, 400]


pipette._aspirate(
    [
        hal.pipette._AspirateDispenseOptions(
            ChannelNumber=1,
            LayoutItem=plate,
            PositionID=position_ids[i],
            WellVolume=well_volumes[i],
            MixCycles=mix_cycles[i],
            MixVolume=mix_volumes[i],
            LiquidClass="HighVolume_Water_DispenseSurface_Empty",
            Volume=volumes[i],
        )
        for i in range(8)
    ],
)

input("enter")

input("enter")

pipette._eject(
    [
        hal.pipette._EjectOptions(
            ChannelNumber=i + 1,
            LabwareID="VStarWaste_16Pos_0001",
            PositionID=str(i + 1),
        )
        for i in range(8)
    ],
)

pipette.deinitialize()

tip.deinitialize()

hamilton_backend.stop()
