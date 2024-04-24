from __future__ import annotations

import os

from loguru import logger

from plh import api, implementation

logger.enable("plh")


implementation.load_yaml_configuration(
    os.path.join(os.path.dirname(__file__), "Config")
)

source = implementation.layout_item.devices["Carrier42_Pos1_Hamilton1500uLFlipTubeRack"]
destination = implementation.layout_item.devices[
    "Centrifuge_Pos1_Hamilton1500uLFlipTubeRack"
]


hamilton_backend = implementation.backend.devices["Hamilton"]
hamilton_backend.start()

gripper = implementation.transport.devices["COREGripper"]
gripper.initialize()

gripper = implementation.transport.devices["TrackGripper"]
gripper.initialize()

api.transport.layout_item_transport(source, destination)
api.transport.layout_item_transport(destination, source)

input("ENTER")

hamilton_backend.stop()
