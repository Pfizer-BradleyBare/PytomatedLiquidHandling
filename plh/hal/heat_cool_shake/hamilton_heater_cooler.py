from __future__ import annotations

from dataclasses import field

from pydantic import dataclasses

from plh.driver.HAMILTON import HamiltonHeaterCooler as HamiltonHeaterCoolerDriver
from plh.driver.HAMILTON.backend import HamiltonBackendBase

from .exceptions import ShakingNotSupportedError
from .heat_cool_shake_base import *
from .heat_cool_shake_base import HeatCoolShakeBase
from .options import HeatCoolShakeOptions


@dataclasses.dataclass(kw_only=True)
class HamiltonHeaterCooler(HeatCoolShakeBase):
    """Hamilton device that can heat and cool."""

    com_port: str
    """Port to communicate with the device 'COM1'."""

    backend: HamiltonBackendBase
    """This device is only supported by Hamilton backends."""

    handle_id: str = field(init=False, default="NONE")
    """Handle id used to perform actions after initialization."""

    def assert_options(
        self: HamiltonHeaterCooler,
        options: HeatCoolShakeOptions,
    ) -> None:
        excepts = []

        try:
            super().assert_options(options)
        except ExceptionGroup as e:
            excepts += e.exceptions

        rpm = options.rpm

        if rpm is not None:
            excepts.append(ShakingNotSupportedError(self))

        if len(excepts) > 0:
            msg = "HeatCoolShakeDevice Options Exceptions"
            raise ExceptionGroup(msg, excepts)

    def initialize(self: HamiltonHeaterCooler) -> None:
        """Connects to Hamilton HeaterCooler device."""
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
        """Stops temperature control on device."""
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

    def set_temperature(
        self: HamiltonHeaterCooler,
        options: HeatCoolShakeOptions,
    ) -> None:
        self.assert_options(options)

        temperature = options.temperature

        assert temperature is not None

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
        options: HeatCoolShakeOptions,
    ) -> float:
        self.assert_options(options)

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

    def set_shaking_speed(
        self: HamiltonHeaterCooler,
        options: HeatCoolShakeOptions,
    ) -> None:
        """Shaking is not supported for this device."""
        self.assert_options(options)

    def get_shaking_speed(self: HamiltonHeaterCooler) -> int:
        """Shaking is not supported for this device. Nonetheless, returns 0"""
        return 0
