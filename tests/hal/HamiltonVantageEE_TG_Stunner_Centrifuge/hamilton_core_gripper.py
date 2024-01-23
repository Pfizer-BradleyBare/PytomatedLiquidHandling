from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("PytomatedLiquidHandling")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

hamilton_backend = hal.backend.devices["Hamilton"]

hamilton_backend.start()

gripper = hal.transport.devices["COREGripper"]

gripper.initialize()

source = hal.layout_item.devices["Carrier48_Pos1_Biorad200uLPCRPlate"]
destination = hal.layout_item.devices["Carrier48_Pos2_Biorad200uLPCRPlate"]

transport_options = hal.transport.TransportOptions(
    source_layout_item=source,
    destination_layout_item=destination,
)

gripper.assert_options(transport_options)

gripper.get(transport_options)

gripper.place(transport_options)

input("ENTER")

gripper.deinitialize()

hamilton_backend.stop()
