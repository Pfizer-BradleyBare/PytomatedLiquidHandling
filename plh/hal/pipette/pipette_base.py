from __future__ import annotations

import copy
from abc import abstractmethod
from math import ceil
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.tools import *
from plh.hal import deck_location, labware
from plh.hal.deck_location import *
from plh.hal.labware import *
from plh.hal.tools import HALDevice, Interface

from .options import (
    TransferOptions,
    _AspirateDispenseOptions,
)
from .pipette_tip import PipetteTip


@dataclasses.dataclass(kw_only=True, eq=False)
class PipetteBase(Interface, HALDevice):
    supported_tips: list[PipetteTip]

    supported_source_labware: Annotated[
        list[labware.PipettableLabware],
        BeforeValidator(labware.validate_list),
    ]
    supported_destination_labware: Annotated[
        list[labware.PipettableLabware],
        BeforeValidator(labware.validate_list),
    ]
    supported_deck_locations: Annotated[
        list[deck_location.DeckLocationBase],
        BeforeValidator(deck_location.validate_list),
    ]

    waste_labware_id: str

    def __post_init__(self:PipetteBase) -> None:
        self.supported_tips = sorted(self.supported_tips,key=lambda x:x.tip.volume)

    def assert_supported_source_labware(
        self: PipetteBase,
        *args: labware.LabwareBase,
    ) -> None:
        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in self.supported_source_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_supported_destination_labware(
        self: PipetteBase,
        *args: labware.LabwareBase,
    ) -> None:
        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in self.supported_destination_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_supported_deck_locations(
        self: PipetteBase,
        *args: deck_location.DeckLocationBase,
    ) -> None:
        exceptions = [
            deck_location.exceptions.DeckLocationNotSupportedError(self, item)
            for item in args
            if item not in self.supported_deck_locations
        ]

        if len(exceptions) != 0:
            msg = "Some deck locations are not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_supported_aspirate_liquid_class_categories(
        self: PipetteBase,
        *args: tuple[str, float],
    ) -> None:
        # TODO
        ...

    def assert_supported_dispense_liquid_class_categories(
        self: PipetteBase,
        *args: tuple[str, float],
    ) -> None:
        # TODO
        ...

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
                for liquid_class in tip.supported_aspirate_liquid_class_categories[
                    source_liquid_class_category
                ]:
                    if liquid_class.max_volume > max_volume:
                        max_volume = liquid_class.max_volume

                for liquid_class in tip.supported_dispense_liquid_class_categories[
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

        for liquid_class in tip.supported_aspirate_liquid_class_categories[
            liquid_class_category
        ]:
            if liquid_class.max_volume > volume:
                return liquid_class.liquid_class_name

        return [
            liquid_class.liquid_class_name
            for liquid_class in tip.supported_aspirate_liquid_class_categories[
                liquid_class_category
            ]
        ][-1]

    @abstractmethod
    def _pickup(
        self: PipetteBase,
        *args: tuple[int, PipetteTip],
    ) -> None:
        """This function should pickup tips from a given pipette tip location."""
        """Errors should be handled here, such that iteration will continue accross tips until either the teir runs out of positions or tips are successfully picked up."""
        ...

    @abstractmethod
    def _eject(
        self: PipetteBase,
        *args: tuple[int, tuple[str, str]],
    ) -> None:
        """This function should eject tips to a positions defined by ```_EjectOptions```."""
        ...

    @abstractmethod
    def _eject_waste(
        self: PipetteBase,
        *args: int,
    ) -> None:
        """This function should eject tips to a positions defined by ```_EjectOptions```."""
        ...

    @abstractmethod
    def _aspirate(
        self: PipetteBase,
        *args: _AspirateDispenseOptions,
    ) -> None: ...

    @abstractmethod
    def _dispense(
        self: PipetteBase,
        *args: _AspirateDispenseOptions,
    ) -> None: ...

    def assert_options(
        self: PipetteBase,
        *args: tuple[TransferOptions,...],
    ) -> None:
        ...

    @abstractmethod
    def transfer(self: PipetteBase, *args: tuple[TransferOptions,...]) -> None:
        """args is a tuple of transfer options.
        The first item in the tuple is the aspirate options.
        The following items in the tuple are dispense options which can support repeat dispensing."""

    @abstractmethod
    def transfer_time(self: PipetteBase, *args: tuple[TransferOptions,...]) -> float:
        """args is a tuple of transfer options.
        The first item in the tuple is the aspirate options.
        The following items in the tuple are dispense options which can support repeat dispensing."""
