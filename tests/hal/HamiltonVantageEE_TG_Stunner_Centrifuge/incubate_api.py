from __future__ import annotations

import os

from loguru import logger

from plh import implementation
from plh.api import deinitialize, incubate, initialize
from plh.api.container import Well
from plh.api.deck_manager import move_container
from plh.api.tools import loaded_labware

logger.enable("plh")

implementation.load_yaml_configuration(
    os.path.join(os.path.dirname(__file__), "Config"),
)

initialize()

biorad = implementation.layout_item.devices["Carrier42_Pos1_Biorad200uLPCRPlate"]

ll = loaded_labware.LoadedLabware(biorad)

well = Well()

ll.create_assignments(well, 1)

reservations = incubate.reserve(50, 0, well)
incubate.start(reservations)
import time

time.sleep(10)
incubate.end(reservations, [biorad.carrier_location])
incubate.release(reservations)

move_container([well], [biorad.carrier_location])

deinitialize()
