from __future__ import annotations

import os

from loguru import logger

from plh import implementation

logger.enable("plh")


implementation.load_yaml_configuration(
    os.path.join(os.path.dirname(__file__), "Config"),
)

hamilton_backend = implementation.backend.devices["Hamilton"]

hamilton_backend.start()

gripper = implementation.transport.devices["COREGripper"]

gripper.initialize()

source = implementation.layout_item.devices["Carrier48_Pos1_Biorad200uLPCRPlate"]
destination = implementation.layout_item.devices["Carrier48_Pos1_Biorad200uLPCRPlate"]


gripper.assert_supported_labware(source.labware, destination.labware)
gripper.assert_supported_carrier_locations(
    source.carrier_location,
    destination.carrier_location,
)
gripper.assert_compatible_carrier_locations(
    source.carrier_location,
    destination.carrier_location,
)
for i in range(10):
    gripper.transport(source, destination)


input("ENTER")

gripper.deinitialize()

hamilton_backend.stop()
