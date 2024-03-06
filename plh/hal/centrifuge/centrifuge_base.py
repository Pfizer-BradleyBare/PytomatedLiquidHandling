from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import labware
from plh.hal import layout_item as li
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True, eq=False)
class CentrifugeBase(Interface, HALDevice):
    """On deck centrifuge that can be accessed by a liquid handler."""

    filter_plate_stacks: Annotated[
        list[li.FilterPlateStack],
        BeforeValidator(li.validate_list),
    ]
    """The acceptable filter plate stacks supported by the centrifuge."""

    def assert_supported_labware(
        self: CentrifugeBase,
        *args: tuple[labware.LabwareBase, labware.LabwareBase],
    ) -> None:
        supported_labware = [
            (item.filter_plate.labware, item.base.labware)
            for item in self.filter_plate_stacks
        ]

        exceptions = [
            labware.exceptions.LabwareStackNotSupportedError(self, *item)
            for item in args
            if item not in supported_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def get_layout_item(
        self: CentrifugeBase,
        stack_labware: tuple[labware.LabwareBase, labware.LabwareBase],
    ) -> li.FilterPlateStack:
        """Gets a layout item on the centrifuge device that is compatible with your current labware stack."""
        self.assert_supported_labware(stack_labware)

        filter_labware, base_labware = stack_labware

        for supported_layout_item in self.filter_plate_stacks:
            if (
                supported_layout_item.filter_plate.labware == filter_labware
                and supported_layout_item.base.labware == base_labware
            ):
                return supported_layout_item

        msg = "Should never reach this point."
        raise RuntimeError(msg)

    @abstractmethod
    def get_bucket_pattern(self: CentrifugeBase, num_buckets: int) -> list[int]:
        """With centrifuges with many buckets it may be possible to load odd numbers of stacks.
        This will account for the bucket configuration and attempt to support your number of buckets required.
        Will return a list of bucket indices to load in any order.
        """
        ...

    @abstractmethod
    def select_bucket(self: CentrifugeBase, index: int) -> None:
        """Exposes a bucket to be loaded. Will not return until bucket is fully exposed."""

    @abstractmethod
    def select_bucket_time(self: CentrifugeBase, index: int) -> float:
        """Time required to expose a bucket."""

    @abstractmethod
    def close(self: CentrifugeBase) -> None:
        """Closes the centrifuge. Will not return until fully closed."""

    @abstractmethod
    def close_time(self: CentrifugeBase) -> float:
        """Time to close the centrifuge."""

    @abstractmethod
    def spin(
        self: CentrifugeBase,
        xG: float,
        accel_percent: float,
        decel_percent: float,
    ) -> None:
        """Starts the centrifuge with a given G force and accel decel percentage."""

    @abstractmethod
    def stop(self: CentrifugeBase) -> None:
        """Stop the centrifuge. Will not return until fully stopped."""

    @abstractmethod
    def stop_time(self: CentrifugeBase) -> float:
        """Time to stop the centrifuge."""

    @abstractmethod
    def is_spinning(self: CentrifugeBase) -> bool:
        """Self explanatory."""
