from __future__ import annotations

import os

from loguru import logger

from plh import hal
from plh.hal.pipette import AspirateOptions, DispenseOptions

logger.enable("plh")

hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))


li1 = hal.layout_item.devices["Carrier48_Pos1_Biorad200uLPCRPlate"]
li2 = hal.layout_item.devices["Carrier48_Pos2_Biorad200uLPCRPlate"]
li3 = hal.layout_item.devices["Carrier48_Pos3_Biorad200uLPCRPlate"]
li4 = hal.layout_item.devices["Carrier48_Pos4_Biorad200uLPCRPlate"]
p = hal.pipette.devices["Pipette"]

a = AspirateOptions(
    layout_item=li1,
    position=1,
    current_volume=1,
    mix_cycles=0,
    liquid_class_category="Test",
)
d = DispenseOptions(
    layout_item=li2,
    position=1,
    current_volume=1,
    mix_cycles=0,
    liquid_class_category="Test",
    transfer_volume=100,
)

opts = (a, d, d, d, d, d)

p.transfer(opts)

print(p._get_supported_tips(*opts)[-1].tip.identifier)
