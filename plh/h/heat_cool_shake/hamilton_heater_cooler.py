from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, Literal

from pydantic import dataclasses

from plh.driver.HAMILTON import HamiltonHeaterCooler as HamiltonHeaterCoolerDriver

from .exceptions import ShakingNotSupportedError
from .heat_cool_shake_base import HeatCoolShakeBase

if TYPE_CHECKING:
    from plh.driver.HAMILTON.backend import HamiltonBackendBase
    from plh.hal import layout_item as li


@dataclasses.dataclass(kw_only=True)
class HamiltonHeaterCooler(HeatCoolShakeBase):
    com_port: str
    backend: HamiltonBackendBase
    backend_error_handling: Literal["N/A"] = "N/A"

    handle_id: str = field(init=False)

    def assert_options(
        self: HamiltonHeaterCooler,
        layout_item: li.LayoutItemBase,
        temperature: float | None = None,
        rpm: int | None = None,
    ) -> None:
        excepts = []

        try:
            super().assert_options(layout_item, temperature, rpm)
        except ExceptionGroup as e:
            excepts += e.exceptions

        if rpm is not None:
            excepts.append(ShakingNotSupportedError)

        if len(excepts) > 0:
            msg = "HeatCoolShakeDevice Options Exceptions"
            raise ExceptionGroup(msg, excepts)

    def initialize(self: HamiltonHeaterCooler) -> None:
        HeatCoolShakeBase.initialize(self)

        command = HamiltonHeaterCoolerDriver.Connect.Command(
            options=HamiltonHeaterCoolerDriver.Connect.Options(
                ComPort=self.com_port,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(
            command,
            HamiltonHeaterCoolerDriver.Connect.Response,
        )

        self._HandleID = response.HandleID

    def deinitialize(self: HamiltonHeaterCooler) -> None:
        HeatCoolShakeBase.deinitialize(self)

        command = HamiltonHeaterCoolerDriver.StopTemperatureControl.Command(
            options=HamiltonHeaterCoolerDriver.StopTemperatureControl.Options(
                HandleID=str(self._HandleID),
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HamiltonHeaterCoolerDriver.StopTemperatureControl.Response,
        )

    def set_temperature(self: HamiltonHeaterCooler, temperature: float) -> None:
        command = HamiltonHeaterCoolerDriver.SetTemperature.Command(
            options=HamiltonHeaterCoolerDriver.SetTemperature.Options(
                HandleID=str(self.handle_id),
                Temperature=temperature,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HamiltonHeaterCoolerDriver.SetTemperature.Response,
        )

    def time_to_temperature(self: HamiltonHeaterCooler, temperature: float) -> float:
        return 0

    def get_temperature(
        self: HamiltonHeaterCooler,
    ) -> float:
        command = HamiltonHeaterCoolerDriver.GetTemperature.Command(
            options=HamiltonHeaterCoolerDriver.GetTemperature.Options(
                HandleID=str(self._HandleID),
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(
            command,
            HamiltonHeaterCoolerDriver.GetTemperature.Response,
        )

        return response.Temperature

    def set_shaking_speed(self: HamiltonHeaterCooler, rpm: int) -> None:
        raise ShakingNotSupportedError

    def get_shaking_speed(self: HamiltonHeaterCooler) -> int:
        raise ShakingNotSupportedError
