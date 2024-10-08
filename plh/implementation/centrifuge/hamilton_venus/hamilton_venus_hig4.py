from __future__ import annotations

import time
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.device.hamilton_venus import HSLHiGCentrifugeLib
from plh.device.hamilton_venus.backend import HamiltonBackendBase
from plh.implementation import backend
from plh.implementation import layout_item as li

from ..centrifuge_base import CentrifugeBase
from ..exceptions import GForceOutOfRangeError, InvalidBucketNumberError


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusHiG4(CentrifugeBase):
    """Hamilton implementation of the Bionex Hig4 centrifuge."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """Only Hamilton backends."""

    plates: Annotated[
        list[
            li.hamilton_venus.HamiltonVenusPlate
            | li.hamilton_venus.HamiltonVenusCoverablePlate
            | li.hamilton_venus.HamiltonVenusFilterPlate
            | li.hamilton_venus.HamiltonVenusCoverableFilterPlate
        ],
        BeforeValidator(li.validate_list),
    ]

    adapter_id: str
    """Bionex adapter ID as determined by the USB CAN application provided by Bionex."""

    def initialize(self: HamiltonVenusHiG4) -> None:
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

    def deinitialize(self: HamiltonVenusHiG4) -> None:
        self.select_bucket(0)
        # Open the centrifuge before we disconnect. The centrifuge should be stored open.

        command = HSLHiGCentrifugeLib.Disconnect.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.Disconnect.Response)

    def assert_num_buckets(self: HamiltonVenusHiG4, num_buckets: int) -> None:
        if num_buckets != 2:
            raise InvalidBucketNumberError(self, num_buckets, 2)

    def get_bucket_pattern(self: HamiltonVenusHiG4, num_buckets: int) -> list[int]:
        self.assert_num_buckets(num_buckets)

        return [0, 1]

    def select_bucket(self: HamiltonVenusHiG4, index: int) -> None:
        command = HSLHiGCentrifugeLib.OpenShield.Command(
            options=HSLHiGCentrifugeLib.OpenShield.Options(BucketIndex=index),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.OpenShield.Response)

    def select_bucket_time(self: HamiltonVenusHiG4, index: int) -> float:
        return 30

    def close(self: HamiltonVenusHiG4) -> None:
        command = HSLHiGCentrifugeLib.CloseShield.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.CloseShield.Response)

    def close_time(self: HamiltonVenusHiG4) -> float:
        return 30

    def assert_xG(self: CentrifugeBase, xG: float) -> None:
        max_xG = 5000

        if xG > max_xG:
            raise GForceOutOfRangeError(self, xG, max_xG)

    def spin(
        self: HamiltonVenusHiG4,
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

    def stop(self: HamiltonVenusHiG4) -> None:
        command = HSLHiGCentrifugeLib.AbortSpin.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLHiGCentrifugeLib.AbortSpin.Response)

        while self.is_spinning():
            time.sleep(5)

    def stop_time(self: HamiltonVenusHiG4) -> float:
        return 30

    def is_spinning(self: HamiltonVenusHiG4) -> bool:
        command = HSLHiGCentrifugeLib.IsSpinning.Command()
        self.backend.execute(command)
        self.backend.wait(command)
        return self.backend.acknowledge(
            command,
            HSLHiGCentrifugeLib.IsSpinning.Response,
        ).IsSpinning
