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

pipette.transfer(
    [
        hal.pipette.TransferOptions(
            source_layout_item=plate,
            source_position=i + 1,
            source_well_volume=100,
            source_mix_cycles=0,
            source_liquid_class_category="Test",
            destination_layout_item=plate,
            destination_position=i + 1,
            destination_well_volume=200,
            destination_mix_cycles=0,
            destination_liquid_class_category="Test",
            transfer_volume=100,
        )
        for i in range(24)
    ]
),

pipette.deinitialize()

tip.deinitialize()

hamilton_backend.stop()
