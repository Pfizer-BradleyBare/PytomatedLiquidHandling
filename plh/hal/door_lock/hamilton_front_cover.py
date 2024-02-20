from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import ML_STAR
from plh.hal import backend

from .door_lock_base import *
from .door_lock_base import DoorLockBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonFrontCover(DoorLockBase):
    """Main Hamilton door locks."""

    backend: Annotated[
        HamiltonBackendBase,
        BeforeValidator(backend.validate_instance),
    ]

    def initialize(self: HamiltonFrontCover) -> None:
        """No initialization required."""

    def deinitialize(self: HamiltonFrontCover) -> None:
        """No deinitialization required."""

    def unlock(self: HamiltonFrontCover) -> None:
        """Unlocks Hamilton sash."""
        command = ML_STAR.LockUnlockFrontCover.Command(
            backend_error_handling=True,
            options=ML_STAR.LockUnlockFrontCover.Options(
                LockState=ML_STAR.LockUnlockFrontCover.LockStateOptions.Unlocked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, ML_STAR.LockUnlockFrontCover.Response)

    def lock(self: HamiltonFrontCover) -> None:
        """Locks Hamilton sash."""
        command = ML_STAR.LockUnlockFrontCover.Command(
            backend_error_handling=True,
            options=ML_STAR.LockUnlockFrontCover.Options(
                LockState=ML_STAR.LockUnlockFrontCover.LockStateOptions.Locked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, ML_STAR.LockUnlockFrontCover.Response)
