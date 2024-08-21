from __future__ import annotations

from dataclasses import field
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.device.HAMILTON import HamiltonHeaterCooler as HamiltonHeaterCoolerDriver
from plh.device.HAMILTON.backend import HamiltonBackendBase
from plh.implementation import backend

from .exceptions import ShakingNotSupportedError
from .heat_cool_shake_base import HeatCoolShakeBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonHeaterCooler(HeatCoolShakeBase):
    """Hamilton device that can heat and cool."""

    com_port: str
    """Port to communicate with the device 'COM1'."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """This device is only supported by Hamilton backends."""

    handle_id: str = field(init=False, default="NONE")
    """Handle id used to perform actions after initialization."""

    def initialize(self: HamiltonHeaterCooler) -> None:
        """Connects to Hamilton HeaterCooler device."""
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
        """Stops temperature control on device."""
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

    def assert_temperature(
        self: HamiltonHeaterCooler,
        temperature: float,
    ) -> None: ...

    def set_temperature(
        self: HamiltonHeaterCooler,
        temperature: float,
    ) -> None:
        self.assert_temperature(temperature)

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

    def set_temperature_time(
        self: HamiltonHeaterCooler,
        temperature: float,
    ) -> float:
        self.assert_temperature(temperature)

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

    def assert_rpm(
        self: HamiltonHeaterCooler,
        rpm: float,
    ) -> None:
        if rpm != 0:
            raise ShakingNotSupportedError(self)

    def set_shaking_speed(
        self: HamiltonHeaterCooler,
        rpm: float,
    ) -> None:
        """Shaking is not supported for this device."""
        self.assert_rpm(rpm)

    def get_shaking_speed(self: HamiltonHeaterCooler) -> int:
        """Shaking is not supported for this device. Nonetheless, returns 0"""
        return 0
