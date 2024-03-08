from __future__ import annotations

from .hamilton_portrait_core8 import HamiltonPortraitCORE8
from .hamilton_portrait_core8_contact_dispense import (
    HamiltonPortraitCORE8ContactDispense,
)

if True:
    pass
# This MUST come first so the if statement ensures that it does not get reordered by a formatter

from .hamilton_core96 import HamiltonCORE96
from .liquid_class import LiquidClass
from .options import TransferOptions, _AspirateDispenseOptions
from .pipette_base import PipetteBase
from .pipette_tip import PipetteTip
from .pydantic_validators import validate_instance

if True:
    from . import exceptions


__all__ = [
    "PipetteBase",
    "PipetteTip",
    "LiquidClass",
    "TransferOptions",
    "_AspirateDispenseOptions",
    "validate_instance",
    "_PickupOptions",
    "HamiltonPortraitCORE8",
    "HamiltonPortraitCORE8ContactDispense",
    "HamiltonCORE96",
    "exceptions",
]

identifier = str
devices: dict[identifier, PipetteBase] = {}
