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
destination = hal.layout_item.devices["Carrier48_Pos2_Biorad200uLPCRPlate"]

transport_options = hal.transport.GetPlaceOptions(
    source_layout_item=source,
    destination_layout_item=destination,
)

gripper.assert_supported_labware([source.labware, destination.labware])
gripper.assert_supported_deck_locations(
    [source.deck_location, destination.deck_location]
)
gripper.assert_compatible_deck_locations(
    source.deck_location, destination.deck_location
)

gripper.get(transport_options)

gripper.place(transport_options)

input("ENTER")

gripper.deinitialize()

hamilton_backend.stop()
