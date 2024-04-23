from __future__ import annotations

from dataclasses import dataclass

from plh.hal.exceptions import HALError

from .centrifuge_base import CentrifugeBase


@dataclass
class GForceOutOfRangeError(HALError):
    """Selected centrifuge can not reach the G force."""

    error_device: CentrifugeBase

    requested_xG: float

    max_xG: float


@dataclass
class InvalidBucketNumberError(HALError):
    """Selected centrifuge does not have enough buckets or can not cleverly load the centrifuge."""

    error_device: CentrifugeBase

    requested_num_buckets: int

    available_num_buckets: int
