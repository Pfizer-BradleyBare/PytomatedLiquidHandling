from __future__ import annotations

import os

from loguru import logger

from plh import hal
from plh.api.deck.container import Liquid, LiquidVolume, PropertyWeight, Viscosity, Well
from plh.api.deck.loader import Criteria, group

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))


IAA_liquid = Liquid("IAA")
TCEP_liquid = Liquid("TCEP",viscosity_property=PropertyWeight(Viscosity.HIGH,1))

IAA = Well([LiquidVolume(IAA_liquid,100),LiquidVolume(IAA_liquid,100)])
print(IAA.get_total_volume())
print(IAA.get_well_property(lambda x:x.viscosity_property))

c = Criteria()

group([c])


input("ENTER")
