from __future__ import annotations

from pydantic import dataclasses

from plh.driver.tools import *
from plh.hal import layout_item
from plh.hal.deck_location import *
from plh.hal.labware import *

from .pipette_tip import PipetteTip


@dataclasses.dataclass(kw_only=True)
class _PickupOptions:
    """Options used for low level ```_pickup``` function."""

    channel_number: int
    """Channel to use to pickup the tip"""

    pipette_tip: PipetteTip
    """Which ```PipetteTip``` to try to pickup."""


@dataclasses.dataclass(kw_only=True)
class _AspirateDispenseOptions:
    """Options use for low level ```_aspirate``` and ```_dispense``` functions."""

    channel_number: int
    "Channel to use for aspiration / dispense"

    layout_item: layout_item.LayoutItemBase
    "Layout item to aspirate /dispense from"

    position_id: str
    "PositionID in the layout item"

    well_volume: float
    """Present volume in the well"""

    mix_cycles: int
    """Cycles to mix. 0 if not needed."""

    mix_volume: float
    """Only matter if ```MixCycles``` is greater than 0. Must be less than or equal to ```WellVolume```."""

    liquid_class: str
    """Liquid class name for aspiration / dispense."""

    volume: float
    """Volume to aspirate / dispense."""


@dataclasses.dataclass(kw_only=True)
class _EjectOptions:
    """Options used for low level ```_eject``` function."""

    channel_number: int
    """Channel to eject."""

    labware_id: str
    """Labware ID to eject into."""

    position_id: str
    """Position ID in labware id to eject into."""


@dataclasses.dataclass(kw_only=True)
class TransferOptions:
    """Options that can be used for ```transfer``` and ```transfer_time```."""

    source_layout_item: layout_item.LayoutItemBase
    """What layout item we are aspirating from."""

    source_position: int | str
    """What position in the ```source_layout_item``` we are aspirating from.
    NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly."""

    source_well_volume: float
    """Current volume in ```source_position``` of ```source_layout_item```."""

    source_mix_cycles: int
    """Cycles to mix before aspiration."""

    source_liquid_class_category: str
    """What liquid class category to use for aspiration."""

    source_sample_group: int | None = None
    """This indicates that the sources with the same sample group number have the exact same solution composition.
    So no contamination will occur upon multiple aspiration.
    NOTE: If ```source_sample_group``` and ```destination_sample_group``` match then the device will assume they are the same as well."""

    destination_layout_item: layout_item.LayoutItemBase
    """What layout item we are dispensing to."""

    destination_position: int | str
    """What position in the ```destination_layout_item``` we are dispensing to.
    NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly."""

    destination_well_volume: float
    """Current volume in ```destination_position``` of ```destination_layout_item```."""

    destination_mix_cycles: int
    """Cycles to mix after dispense."""

    destination_liquid_class_category: str
    """What liquid class category to use for dispense."""

    destination_sample_group: int | None = None
    """This indicates that the destinations with the same sample group number have the exact same solution composition.
    So no contamination will occur upon multiple dispense.
    NOTE: If ```source_sample_group``` and ```destination_sample_group``` match then the device will assume they are the same as well."""

    transfer_volume: float
    """Volume that is transfered from source to destination."""
