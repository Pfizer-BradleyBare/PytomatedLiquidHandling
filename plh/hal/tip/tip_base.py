from __future__ import annotations

from abc import abstractmethod
from dataclasses import field

from pydantic import dataclasses, field_validator

from plh.hal import layout_item
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class AvailablePosition:
    LabwareID: str
    PositionID: str


@dataclasses.dataclass(kw_only=True)
class TipBase(Interface, HALDevice):
    tip_racks: list[layout_item.TipRack]
    tips_per_rack: int
    volume: float
    available_positions: list[AvailablePosition] = field(
        init=False,
        default_factory=list,
    )

    @field_validator("TipRacks", mode="before")
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
        Interface.initialize(self)

    def get_tips(self: TipBase, num: int) -> list[AvailablePosition]:
        if len(self._AvailablePositions) < num:
            msg = "Not enough tips available"
            raise RuntimeError(msg)

        tips = self._AvailablePositions[:num]
        self._AvailablePositions = self._AvailablePositions[num:]
        return tips

    def remaining_tips(self: TipBase) -> int:
        """Total number of tips.
        NOTE: This is not guarenteed to be the number of accessible tips. Call RemainingTipsInTier for that info.
        """
        return len(self._AvailablePositions)

    @abstractmethod
    def update_available_positions(self: TipBase) -> None:
        """This initiates a update of the available positions. This is not neccesarily the same as Initialize"""

    @abstractmethod
    def remaining_tips_in_tier(self: TipBase) -> int:
        """Total number of accessible tips."""
        ...

    @abstractmethod
    def discard_layer_to_waste(self: TipBase) -> None:
        """For stacked tips, discards the uppermost layer to make the next layer accessible.

        For non-stacked tips, should probably request a tip reload from the user.
        """
        ...