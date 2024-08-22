from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import labware
from plh.implementation import layout_item as li
from plh.implementation.tools import Interface, Resource


@dataclasses.dataclass(kw_only=True, eq=False)
class CentrifugeBase(Resource, Interface):
    """On deck centrifuge that can be accessed by a liquid handler."""

    plates: Annotated[
        list[li.Plate | li.CoverablePlate | li.FilterPlateStack],
        BeforeValidator(li.validate_list),
    ]
    """The acceptable filter plate stacks supported by the centrifuge."""

    def assert_supported_labware(
        self: CentrifugeBase,
        *args: labware.LabwareBase,
    ) -> None:
        supported_labware = [
            item.labware if isinstance(item, li.Plate) else item.filter_plate.labware
            for item in self.plates
        ]

        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in supported_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def get_layout_item(
        self: CentrifugeBase,
        labware: labware.LabwareBase,
    ) -> li.Plate | li.CoverablePlate | li.FilterPlateStack:
        """Gets a layout item on the centrifuge device that is compatible with your current labware stack."""
        self.assert_supported_labware(labware)

        for supported_layout_item in self.plates:
            supported_labware = (
                supported_layout_item.labware
                if isinstance(supported_layout_item, li.Plate)
                else supported_layout_item.filter_plate.labware
            )

            if labware == supported_labware:
                return supported_layout_item

        msg = "Should never reach this point."
        raise RuntimeError(msg)

    @abstractmethod
    def assert_num_buckets(self: CentrifugeBase, num_buckets: int) -> None:
        """Confirm that the number of requested buckets is supported by the centrifuge."""
        ...

    @abstractmethod
    def get_bucket_pattern(self: CentrifugeBase, num_buckets: int) -> list[int]:
        """Centrifuges with many buckets may be possible to load odd numbers of stacks.
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
    def assert_xG(self: CentrifugeBase, xG: float) -> None:
        """Test that the xG is possible with this centrifuge."""
        ...

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
