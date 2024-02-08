from __future__ import annotations

from abc import abstractmethod
from dataclasses import field

from pydantic import dataclasses, field_validator

from plh.hal import layout_item, transport
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class AvailablePosition:
    """A tip position."""

    LabwareID: str
    """The labware id for the position."""

    PositionID: str
    """The position id for the position."""


@dataclasses.dataclass(kw_only=True)
class TipBase(Interface, HALDevice):
    """A tip device that facilitates tip tracking and tier removal as needed."""

    tip_racks: list[layout_item.TipRack]
    """Rack layout items associated with the device."""

    volume: float
    """Tip volume."""

    available_positions: list[AvailablePosition] = field(
        init=False,
        default_factory=list,
    )
    """Tip positions that are immediately available for use."""

    @field_validator("tip_racks", mode="before")
    @classmethod
    def __tip_racks_validate(
        cls: type[TipBase],
        v: list[str | layout_item.LayoutItemBase],
    ) -> list[layout_item.LayoutItemBase]:
        supported_objects = []

        objects = layout_item.devices

        for item in v:
            if isinstance(item, layout_item.LayoutItemBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + layout_item.LayoutItemBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

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

    def initialize(self: TipBase) -> None:
        """Initiates a user update of the available tip positions then stores in the device using the ```update_available_positions``` instance method."""
        self.update_available_positions()

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
    def discard_teir(self: TipBase) -> list[transport.GetPlaceOptions]:
        """Returns a list of transport options to discard the current teir."""
        ...

    @abstractmethod
    def update_available_positions(self: TipBase) -> None:
        """Initiates an update of the available positions. This is not neccesarily the same as Initialize"""
