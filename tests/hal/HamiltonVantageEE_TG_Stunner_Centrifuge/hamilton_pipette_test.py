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
        hal.pipette._PickupOptions(channel_number=1, pipette_tip=pipette_tip),
        hal.pipette._PickupOptions(channel_number=2, pipette_tip=pipette_tip),
        hal.pipette._PickupOptions(channel_number=3, pipette_tip=pipette_tip),
        hal.pipette._PickupOptions(channel_number=4, pipette_tip=pipette_tip),
        hal.pipette._PickupOptions(channel_number=5, pipette_tip=pipette_tip),
        hal.pipette._PickupOptions(channel_number=6, pipette_tip=pipette_tip),
        hal.pipette._PickupOptions(channel_number=7, pipette_tip=pipette_tip),
        hal.pipette._PickupOptions(channel_number=8, pipette_tip=pipette_tip),
    ],
)

input("enter")

position_ids = ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"]
well_volumes = [5, 25, 50, 100, 150, 200, 300, 400]
volumes = [5, 25, 50, 100, 150, 200, 300, 400]
mix_cycles = [0, 0, 0, 5, 0, 0, 0, 5]
mix_volumes = [0, 0, 0, 150, 0, 0, 0, 200]


pipette._aspirate(
    [
        hal.pipette._AspirateDispenseOptions(
            channel_number=i + 1,
            layout_item=plate,
            position_id=position_ids[i],
            well_volume=well_volumes[i],
            mix_cycles=mix_cycles[i],
            mix_volume=mix_volumes[i],
            liquid_class="HighVolume_Water_DispenseSurface_Empty",
            volume=volumes[i],
        )
        for i in range(8)
    ],
)

input("enter")

input("enter")

pipette._eject(
    [
        hal.pipette._EjectOptions(
            channel_number=i + 1,
            labware_id="VStarWaste_16Pos_0001",
            position_id=str(i + 1),
        )
        for i in range(8)
    ],
)

pipette.deinitialize()

tip.deinitialize()

hamilton_backend.stop()
