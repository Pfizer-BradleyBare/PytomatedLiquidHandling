from __future__ import annotations

from abc import abstractmethod
from dataclasses import field
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import layout_item
from plh.implementation.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class AvailablePosition:
    """A tip position."""

    LabwareID: str
    """The labware id for the position."""

    PositionID: str
    """The position id for the position."""


@dataclasses.dataclass(kw_only=True, eq=False)
class TipBase(Interface, HALDevice):
    """A tip device that facilitates tip tracking and tier removal as needed."""

    tip_racks: Annotated[
        list[layout_item.TipRack],
        BeforeValidator(layout_item.validate_list),
    ]
    """Rack layout items associated with the device."""

    volume: float
    """Tip volume."""

    available_positions: list[AvailablePosition] = field(
        init=False,
        default_factory=list,
    )
    """Tip positions that are immediately available for use."""

    def _parse_available_positions(
        self: TipBase,
        available_positions: list[dict[str, str]],
    ) -> None:
        for pos in available_positions:
            self.available_positions.append(
                AvailablePosition(
                    LabwareID=pos["LabwareID"],
                    PositionID=pos["PositionID"],
                ),
            )

    @abstractmethod
    def initialize(self: TipBase) -> None:
        """Initiates a user update of the available tip positions then stores in the device using the ```update_available_positions``` instance method."""

    def use_tips(self: TipBase, num: int) -> None:
        """Indicates that the following number of tips have been used and are no longer available."""
        self.available_positions = self.available_positions[num:]

    @abstractmethod
    def remaining_tips(self: TipBase) -> int:
        """Total number of tips.
        NOTE: This is not guarenteed to be the number of accessible tips. Call RemainingTipsInTier for that info.
        """
        ...

    @abstractmethod
    def discard_teir(
        self: TipBase,
    ) -> None:
        """Uses the compatible transport device to discard the teir."""
        ...

    @abstractmethod
    def update_available_positions(
        self: TipBase,
        raw_available_positions: list[dict[str, str]],
    ) -> None:
        """Initiates an update of the available positions. This is not neccesarily the same as Initialize"""
