from __future__ import annotations

import copy
from abc import abstractmethod
from math import ceil

from pydantic import dataclasses, field_validator

from plh.driver.tools import *
from plh.hal import deck_location, labware, layout_item
from plh.hal.deck_location import *
from plh.hal.labware import *
from plh.hal.tools import HALDevice, Interface

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


@dataclasses.dataclass(kw_only=True)
class PipetteBase(Interface, HALDevice):
    supported_tips: list[PipetteTip]
    supported_source_labware: list[labware.PipettableLabware]
    supported_destination_labware: list[labware.PipettableLabware]
    supported_deck_locations: list[deck_location.DeckLocationBase]

    @field_validator("supported_tips", mode="after")
    @classmethod
    def __supported_tips_validate(
        cls: type[PipetteBase],
        v: list[PipetteTip],
    ) -> list[PipetteTip]:
        return sorted(v, key=lambda x: x.tip.volume)

    @field_validator("supported_deck_locations", mode="before")
    @classmethod
    def __supported_deck_locations_validate(
        cls: type[PipetteBase],
        v: list[str | deck_location.DeckLocationBase],
    ) -> list[deck_location.DeckLocationBase]:
        supported_objects = []

        objects = deck_location.devices

        for item in v:
            if isinstance(item, deck_location.DeckLocationBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + deck_location.DeckLocationBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

    @field_validator(
        "supported_source_labware",
        "supported_destination_labware",
        mode="before",
    )
    @classmethod
    def __supported_labwares_validate(
        cls: type[PipetteBase],
        v: list[str | labware.LabwareBase],
    ) -> list[labware.LabwareBase]:
        supported_objects = []

        objects = labware.devices

        for item in v:
            if isinstance(item, labware.LabwareBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + labware.LabwareBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

    def assert_options(
        self: PipetteBase,
        options: list[TransferOptions],
    ) -> None:
        unsupported_deck_locations = []
        unsupported_labware = []
        unsupported_liquid_class_categories = []

        for opt in options:
            source_labware = opt.source_layout_item.labware
            destination_labware = opt.destination_layout_item.labware
            if source_labware not in self.supported_source_labware:
                unsupported_labware.append(source_labware)
            if destination_labware not in self.supported_destination_labware:
                unsupported_labware.append(destination_labware)
            # Check Labware Compatibility

            source_deck_location = opt.source_layout_item.deck_location
            destination_deck_location = opt.destination_layout_item.deck_location
            if source_deck_location not in self.supported_deck_locations:
                unsupported_deck_locations.append(source_deck_location)
            if destination_deck_location not in self.supported_deck_locations:
                unsupported_deck_locations.append(destination_deck_location)
            # Check DeckLocation compatibility

            source_liquid_class_category = opt.source_liquid_class_category
            destination_liquid_class_category = opt.destination_liquid_class_category
            if not any(
                PipetteTip.is_liquid_class_category_supported(
                    source_liquid_class_category,
                )
                for PipetteTip in self.supported_tips
            ):
                unsupported_liquid_class_categories.append(source_liquid_class_category)
            if not any(
                PipetteTip.is_liquid_class_category_supported(
                    destination_liquid_class_category,
                )
                for PipetteTip in self.supported_tips
            ):
                unsupported_liquid_class_categories.append(
                    destination_liquid_class_category,
                )
            # Check liquid class compatibility

    def _get_max_transfer_volume(
        self: PipetteBase,
        source_liquid_class_category: str,
        destination_liquid_class_category: str,
    ) -> float:
        max_volume = 0

        for tip in self.supported_tips:
            if tip.is_liquid_class_category_supported(
                source_liquid_class_category,
            ) and tip.is_liquid_class_category_supported(
                destination_liquid_class_category,
            ):
                for liquid_class in tip.supported_liquid_class_categories[
                    source_liquid_class_category
                ]:
                    if liquid_class.max_volume > max_volume:
                        max_volume = liquid_class.max_volume

                for liquid_class in tip.supported_liquid_class_categories[
                    destination_liquid_class_category
                ]:
                    if liquid_class.max_volume > max_volume:
                        max_volume = liquid_class.max_volume

        return max_volume

    def _truncate_transfer_volume(
        self: PipetteBase,
        options: TransferOptions,
        volume: float,
    ) -> list[TransferOptions]:
        options = copy.copy(options)
        num_transfers = ceil(options.transfer_volume / volume)
        options.transfer_volume /= num_transfers

        return [copy.copy(options) for _ in range(num_transfers)]

    def _get_tip(
        self: PipetteBase,
        source_liquid_class_category: str,
        destination_liquid_class_category: str,
        volume: float,
    ) -> PipetteTip:
        possible_pipette_tips = [
            pipette_tip
            for pipette_tip in self.supported_tips
            if pipette_tip.is_liquid_class_category_supported(
                source_liquid_class_category,
            )
            and pipette_tip.is_liquid_class_category_supported(
                destination_liquid_class_category,
            )
        ]

        for pipette_tip in possible_pipette_tips:
            if pipette_tip.tip.volume >= volume:
                return pipette_tip

        return possible_pipette_tips[-1]

    def _get_liquid_class(
        self: PipetteBase,
        liquid_class_category: str,
        volume: float,
    ) -> str:
        tip = self._get_tip(liquid_class_category, liquid_class_category, volume)

        for liquid_class in tip.supported_liquid_class_categories[
            liquid_class_category
        ]:
            if liquid_class.max_volume > volume:
                return liquid_class.liquid_class_name

        return [
            liquid_class.liquid_class_name
            for liquid_class in tip.supported_liquid_class_categories[
                liquid_class_category
            ]
        ][-1]

    @abstractmethod
    def _pickup(
        self: PipetteBase,
        options: list[_PickupOptions],
    ) -> None:
        """This function should pickup tips from a given pipette tip location."""
        """Errors should be handled here, such that iteration will continue accross tips until either the teir runs out of positions or tips are successfully picked up."""
        ...

    @abstractmethod
    def _eject(
        self: PipetteBase,
        positions: list[_EjectOptions],
    ) -> None:
        """This function should eject tips to a positions defined by ```_EjectOptions```."""
        ...

    @abstractmethod
    def _aspirate(self: PipetteBase, options: list[_AspirateDispenseOptions]) -> None:
        ...

    @abstractmethod
    def _dispense(self: PipetteBase, options: list[_AspirateDispenseOptions]) -> None:
        ...

    @abstractmethod
    def transfer(self: PipetteBase, options: list[TransferOptions]) -> None:
        ...

    @abstractmethod
    def transfer_time(self: PipetteBase, options: list[TransferOptions]) -> float:
        ...
