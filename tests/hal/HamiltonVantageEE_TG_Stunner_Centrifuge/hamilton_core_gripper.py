from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

hamilton_backend = hal.backend.devices["Hamilton"]

hamilton_backend.start()

gripper = hal.transport.devices["COREGripper"]

gripper.initialize()

source = hal.layout_item.devices["Carrier48_Pos1_Biorad200uLPCRPlate"]
destination = hal.layout_item.devices["Carrier48_Pos1_Biorad200uLPCRPlate"]


gripper.assert_supported_labware(source.labware, destination.labware)
gripper.assert_supported_deck_locations(
    source.deck_location,
    destination.deck_location,
)
gripper.assert_compatible_deck_locations(
    source.deck_location,
    destination.deck_location,
)
for i in range(0,10):
    gripper.transport(source, destination)


input("ENTER")

gripper.deinitialize()

hamilton_backend.stop()
