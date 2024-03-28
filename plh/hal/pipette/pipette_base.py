from __future__ import annotations

from abc import abstractmethod
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

    supported_aspirate_labware: Annotated[
        list[labware.PipettableLabware],
        BeforeValidator(labware.validate_list),
    ]
    supported_dispense_labware: Annotated[
        list[labware.PipettableLabware],
        BeforeValidator(labware.validate_list),
    ]
    supported_deck_locations: Annotated[
        list[deck_location.DeckLocationBase],
        BeforeValidator(deck_location.validate_list),
    ]

    waste_labware_id: str

    def __post_init__(self: PipetteBase) -> None:
        self.supported_tips = sorted(self.supported_tips, key=lambda x: x.tip.volume)

    def assert_supported_aspirate_labware(
        self: PipetteBase,
        *args: labware.LabwareBase,
    ) -> None:
        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in self.supported_aspirate_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_supported_dispense_labware(
        self: PipetteBase,
        *args: labware.LabwareBase,
    ) -> None:
        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in self.supported_dispense_labware
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

    def assert_supported_tips(
        self: PipetteBase,
        *args: tuple[TransferOptions, ...],
    ) -> None:
        """Checks that the liquid_class_category and volume is compatible for both dispense and aspirate steps.
        The dispense steps are checked first as those are high priority (because they need to be most accurate)."""

        for arg in args:
            aspirate_option = arg[0]
            dispense_options = arg[1:]

            aspirate_liquid_class_category = aspirate_option.liquid_class_category
            aspirate_volume = aspirate_option.transfer_volume

            dispense_liquid_class_categories = [
                option.liquid_class_category for option in dispense_options
            ]
            dispense_volumes = [option.transfer_volume for option in dispense_options]

            possible_tips: list[PipetteTip] = [
                tip
                for tip in self.supported_tips
                if all(
                    dispense_category in tip.supported_dispense_liquid_class_categories
                    for dispense_category in dispense_liquid_class_categories
                )
            ]
            # We should first try to find a tip that satisfies the dispense volumes and liquid class category

            for possible_tip in possible_tips[:]:
                for category, volume in zip(
                    dispense_liquid_class_categories, dispense_volumes,
                ):
                    flag = False
                    for (
                        liquid_class
                    ) in possible_tip.supported_dispense_liquid_class_categories[
                        category
                    ]:
                        if liquid_class.min_volume <= volume <= liquid_class.max_volume:
                            flag = True
                            break

                    if flag is False:
                        possible_tips.remove(possible_tip)
            # Now, using the tip we need to confirm that the volumes are supported as well.

            possible_tips:list[PipetteTip] = [tip for tip in possible_tips if aspirate_liquid_class_category in tip.supported_aspirate_liquid_class_categories]

            for possible_tip in possible_tips:
                flag = False
                for (
                    liquid_class
                ) in possible_tip.supported_dispense_liquid_class_categories[
                    category
                ]:
                    if liquid_class.min_volume <= aspirate_volume <= liquid_class.max_volume:
                        flag = True
                        break

                if flag is False:
                    possible_tips.remove(possible_tip)
            #Now we need to check if the aspirate options will work.

            if len(possible_tips) == 0:
                raise Exception("No supported tips are capable of supporting this request.")


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
    ) -> None:
        ...

    @abstractmethod
    def _dispense(
        self: PipetteBase,
        *args: _AspirateDispenseOptions,
    ) -> None:
        ...

    def assert_options(
        self: PipetteBase,
        *args: tuple[TransferOptions, ...],
    ) -> None:
        ...

    @abstractmethod
    def transfer(self: PipetteBase, *args: tuple[TransferOptions, ...]) -> None:
        """Args is a tuple of transfer options.
        The first item in the tuple is the aspirate options.
        The following items in the tuple are dispense options which can support repeat dispensing and tip re-use.
        """

    @abstractmethod
    def transfer_time(self: PipetteBase, *args: tuple[TransferOptions, ...]) -> float:
        """Args is a tuple of transfer options.
        The first item in the tuple is the aspirate options.
        The following items in the tuple are dispense options which can support repeat dispensing and tip re-use.
        """
