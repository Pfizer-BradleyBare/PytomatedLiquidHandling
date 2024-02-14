from __future__ import annotations

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import ML_STAR
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class HamiltonFrontCover(HALDevice, Interface):
    """Allows to unlock all doors on a system."""

    backend: HamiltonBackendBase

    def initialize(self: HamiltonFrontCover) -> None:
        """No initialization required."""

    def deinitialize(self: HamiltonFrontCover) -> None:
        """No deinitialization required."""

    def unlock(self: HamiltonFrontCover) -> None:
        """Unlocks door associated with Track Gripper."""
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
        """Locks door associated with Track Gripper."""
        command = ML_STAR.LockUnlockFrontCover.Command(
            backend_error_handling=True,
            options=ML_STAR.LockUnlockFrontCover.Options(
                LockState=ML_STAR.LockUnlockFrontCover.LockStateOptions.Locked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, ML_STAR.LockUnlockFrontCover.Response)
