from __future__ import annotations

import os

from loguru import logger

from plh import implementation

logger.enable("plh")


implementation.load_yaml_configuration(
    os.path.join(os.path.dirname(__file__), "Config")
)


hamilton_backend = implementation.backend.devices["Hamilton"]

hamilton_backend.start()

tip = implementation.tip.devices["1000uL FTR"]

tip.initialize()

plate = implementation.layout_item.devices[
    "Carrier39_Pos1_Hamilton60mLReagentReservoirCarrier"
]

pipette = implementation.pipette.devices["Pipette"]

pipette.initialize()

pipette.transfer(
    [
        implementation.pipette.TransferOptions(
            source_layout_item=plate,
            source_position=int(i / 8) + 1,
            source_well_volume=0,
            source_mix_cycles=0,
            source_liquid_class_category="Test",
            destination_layout_item=plate,
            destination_position=int(i / 8) + 1,
            destination_well_volume=200,
            destination_mix_cycles=0,
            destination_liquid_class_category="Test",
            transfer_volume=100,
        )
        for i in range(1)
    ],
),

pipette.deinitialize()

tip.deinitialize()

hamilton_backend.stop()
