from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON import HSLHiGCentrifugeLib
from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.hal import backend

from .centrifuge_base import *
from .centrifuge_base import CentrifugeBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonHig4(CentrifugeBase):
    """Hamilton implementation of the Bionex Hig4 centrifuge."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """Only Hamilton backends."""

    adapter_id: str
    """Bionex adapter ID as determined by the USB CAN application provided by Bionex."""

    def initialize(self: HamiltonHig4) -> None:
        command = HSLHiGCentrifugeLib.Connect.Command(
            options=HSLHiGCentrifugeLib.Connect.Options(AdapterID=self.adapter_id),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.Connect.Response)

        command = HSLHiGCentrifugeLib.Home.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.Home.Response)

    def deinitialize(self: HamiltonHig4) -> None:
        self.select_bucket(0)
        # Open the centrifuge before we disconnect. The centrifuge should be stored open.

        command = HSLHiGCentrifugeLib.Disconnect.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.Disconnect.Response)

    def get_bucket_pattern(self: HamiltonHig4, num_buckets: int) -> list[int]:
        if num_buckets != 2:
            msg = "Only 2 buckets at a time are supported."
            raise ValueError(msg)

        return [0, 1]

    def select_bucket(self: HamiltonHig4, index: int) -> None:
        command = HSLHiGCentrifugeLib.OpenShield.Command(
            options=HSLHiGCentrifugeLib.OpenShield.Options(BucketIndex=index),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.OpenShield.Response)

    def select_bucket_time(self: HamiltonHig4, index: int) -> float:
        return 30

    def close(self: HamiltonHig4) -> None:
        command = HSLHiGCentrifugeLib.CloseShield.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.CloseShield.Response)

    def close_time(self: HamiltonHig4) -> float:
        return 30

    def spin(
        self: HamiltonHig4,
        xG: float,
        accel_percent: float,
        decel_percent: float,
    ) -> None:
        command = HSLHiGCentrifugeLib.Spin.Command(
            options=HSLHiGCentrifugeLib.Spin.Options(
                GForce=xG,
                AccelerationPercent=accel_percent,
                DecelerationPercent=decel_percent,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.Spin.Response)

    def stop(self: HamiltonHig4) -> None:
        command = HSLHiGCentrifugeLib.AbortSpin.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.AbortSpin.Response)

    def stop_time(self: HamiltonHig4) -> float:
        return 30

    def is_spinning(self: HamiltonHig4) -> bool:
        command = HSLHiGCentrifugeLib.IsSpinning.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        return self.backend.acknowledge(
            command,
            HSLHiGCentrifugeLib.IsSpinning.Response,
        ).IsSpinning
