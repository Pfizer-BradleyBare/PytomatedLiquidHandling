from __future__ import annotations

import os

from loguru import logger

from plh import api, hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

source = hal.layout_item.devices["Carrier42_Pos1_Hamilton1500uLFlipTubeRack"]
destination = hal.layout_item.devices["Centrifuge_Pos1_Hamilton1500uLFlipTubeRack"]


hamilton_backend = hal.backend.devices["Hamilton"]
hamilton_backend.start()

gripper = hal.transport.devices["COREGripper"]
gripper.initialize()

gripper = hal.transport.devices["TrackGripper"]
gripper.initialize()

api.transport.layout_item_transport(source, destination)
api.transport.layout_item_transport(destination, source)

input("ENTER")

hamilton_backend.stop()