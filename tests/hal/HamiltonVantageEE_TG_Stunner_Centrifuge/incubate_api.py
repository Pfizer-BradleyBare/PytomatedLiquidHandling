from __future__ import annotations

import os

from loguru import logger

from plh import hal
from plh.api import incubate
from plh.api.container import Well
from plh.api.tools import loaded_labware

logger.enable("plh")

hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

biorad = hal.layout_item.devices["Carrier42_Pos1_Biorad200uLPCRPlate"]

ll = loaded_labware.LoadedLabware(biorad)

well = Well()

ll.create_assignments(well, 1)

incubate.assert_compatible_device(50, 0, biorad.labware)
reservation = incubate.reserve(50, 0, well)[0]
incubate.start(reservation)
incubate.release(reservation)