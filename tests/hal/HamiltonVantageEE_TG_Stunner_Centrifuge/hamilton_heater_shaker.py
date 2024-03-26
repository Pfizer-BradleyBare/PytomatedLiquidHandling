from __future__ import annotations

from plh.api import container

#
#
# Define our liquids
#
#
Water = container.Liquid("Water")
ACN = container.Liquid(
    "ACN",
    volatility=(container.Volatility.HIGH, 5),
    viscosity=(container.Viscosity.LOW, 5),
)
Glycerol = container.Liquid(
    "Glycerol",
    volatility=(container.Volatility.LOW, 10),
    viscosity=(container.Viscosity.HIGH, 10),
)

#
#
# Our test wells
#
#
Water_ACN_Well = container.Well((Water, 500))
print(Water_ACN_Well.get_well_property(lambda x: x.volatility))  # Medium
Water_ACN_Well.dispense([(ACN, 150)])
print(Water_ACN_Well.get_well_property(lambda x: x.volatility))  # High

Water_Glycerol_Well = container.Well((Water, 500))
print(Water_Glycerol_Well.get_well_property(lambda x: x.viscosity))  # Medium
Water_Glycerol_Well.dispense([(Glycerol, 100)])
print(Water_Glycerol_Well.get_well_property(lambda x: x.viscosity))  # High
