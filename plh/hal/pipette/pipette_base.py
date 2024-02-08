from __future__ import annotations

import copy
from abc import abstractmethod
from math import ceil

from pydantic import dataclasses, field_validator

from plh.driver.tools import *
from plh.hal import deck_location, labware
from plh.hal.deck_location import *
from plh.hal.labware import *
from plh.hal.tools import HALDevice, Interface

from .options import (
    TransferOptions,
    _AspirateDispenseOptions,
    _EjectOptions,
    _PickupOptions,
)
from .pipette_tip import PipetteTip


@dataclasses.dataclass(kw_only=True)
class PipetteBase(Interface, HALDevice):
    supported_tips: list[PipetteTip]
    supported_source_labware: list[labware.PipettableLabware]
    supported_destination_labware: list[labware.PipettableLabware]
    supported_deck_locations: list[deck_location.DeckLocationBase]

    waste_labware_id: str

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
    def _waste(self: PipetteBase, channel_numbers: list[int]) -> None: ...

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
    def _aspirate(
        self: PipetteBase, options: list[_AspirateDispenseOptions]
    ) -> None: ...

    @abstractmethod
    def _dispense(
        self: PipetteBase, options: list[_AspirateDispenseOptions]
    ) -> None: ...

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

    @abstractmethod
    def transfer(self: PipetteBase, options: list[TransferOptions]) -> None: ...

    @abstractmethod
    def transfer_time(self: PipetteBase, options: list[TransferOptions]) -> float: ...
