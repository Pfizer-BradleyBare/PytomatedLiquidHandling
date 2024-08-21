from __future__ import annotations

from dataclasses import field
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.device.HAMILTON import HSLHamHeaterShakerLib
from plh.device.HAMILTON.backend import HamiltonBackendBase
from plh.implementation import backend

from .exceptions import CoolingNotSupportedError
from .heat_cool_shake_base import HeatCoolShakeBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonHeaterShaker(HeatCoolShakeBase):
    """Hamilton device that can heat and shake."""

    com_port: int
    """Port to communicate with the device '1'."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """This device is only supported by Hamilton backends."""

    handle_id: int = field(init=False, default=0)
    """Handle id used to perform actions after initialization."""

    def initialize(self: HamiltonHeaterShaker) -> None:
        """Connects to the Hamilton HeaterShaker then locks and unlocks the plate lock as a reset mechanism."""
        command = HSLHamHeaterShakerLib.CreateUSBDevice.Command(
            options=HSLHamHeaterShakerLib.CreateUSBDevice.Options(
                ComPort=self.com_port,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.CreateUSBDevice.Response,
        )

        self.handle_id = response.HandleID

        command = HSLHamHeaterShakerLib.SetPlateLock.Command(
            options=HSLHamHeaterShakerLib.SetPlateLock.Options(
                HandleID=self.handle_id,
                PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.LockStateOptions.Locked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.SetPlateLock.Response,
        )

        command = HSLHamHeaterShakerLib.SetPlateLock.Command(
            options=HSLHamHeaterShakerLib.SetPlateLock.Options(
                HandleID=self.handle_id,
                PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.LockStateOptions.Unlocked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.SetPlateLock.Response,
        )

    def deinitialize(self: HamiltonHeaterShaker) -> None:
        """Stops all temperature and shaking control then unlocks the plate lock."""
        command = HSLHamHeaterShakerLib.StopTempCtrl.Command(
            options=HSLHamHeaterShakerLib.StopTempCtrl.Options(
                HandleID=self.handle_id,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.StopTempCtrl.Response,
        )

        command = HSLHamHeaterShakerLib.StopShaker.Command(
            options=HSLHamHeaterShakerLib.StopShaker.Options(
                HandleID=self.handle_id,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.StopShaker.Response,
        )

        command = HSLHamHeaterShakerLib.SetPlateLock.Command(
            options=HSLHamHeaterShakerLib.SetPlateLock.Options(
                HandleID=self.handle_id,
                PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.LockStateOptions.Unlocked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.SetPlateLock.Response,
        )

    def assert_temperature(
        self: HamiltonHeaterShaker,
        temperature: float,
    ) -> None:
        if temperature < 25:
            raise CoolingNotSupportedError(self)

    def set_temperature(
        self: HamiltonHeaterShaker,
        temperature: float,
    ) -> None:
        """Minimum supported temperature is ambient or 25C."""
        self.assert_temperature(temperature)

        command = HSLHamHeaterShakerLib.StartTempCtrl.Command(
            options=HSLHamHeaterShakerLib.StartTempCtrl.Options(
                HandleID=self.handle_id,
                Temperature=temperature,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.StartTempCtrl.Response,
        )

    def set_temperature_time(
        self: HamiltonHeaterShaker,
        temperature: float,
    ) -> float:
        self.assert_temperature(temperature)
        return 0

    def get_temperature(self: HamiltonHeaterShaker) -> float:
        command = HSLHamHeaterShakerLib.GetTemperature.Command(
            options=HSLHamHeaterShakerLib.GetTemperature.Options(
                HandleID=self.handle_id,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.GetTemperature.Response,
        )

        return response.Temperature

    def assert_rpm(
        self: HamiltonHeaterShaker,
        rpm: float,
    ) -> None: ...

    def set_shaking_speed(
        self: HamiltonHeaterShaker,
        rpm: float,
    ) -> None:
        self.assert_rpm(rpm)

        if rpm == 0:
            command = HSLHamHeaterShakerLib.StopShaker.Command(
                options=HSLHamHeaterShakerLib.StopShaker.Options(
                    HandleID=self.handle_id,
                ),
            )
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                HSLHamHeaterShakerLib.StopShaker.Response,
            )

            command = HSLHamHeaterShakerLib.SetPlateLock.Command(
                options=HSLHamHeaterShakerLib.SetPlateLock.Options(
                    HandleID=self.handle_id,
                    PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.LockStateOptions.Unlocked,
                ),
            )
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                HSLHamHeaterShakerLib.SetPlateLock.Response,
            )

        else:
            command = HSLHamHeaterShakerLib.SetPlateLock.Command(
                options=HSLHamHeaterShakerLib.SetPlateLock.Options(
                    HandleID=self.handle_id,
                    PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.LockStateOptions.Locked,
                ),
            )
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                HSLHamHeaterShakerLib.SetPlateLock.Response,
            )

            command = HSLHamHeaterShakerLib.StartShaker.Command(
                options=HSLHamHeaterShakerLib.StartShaker.Options(
                    HandleID=self.handle_id,
                    ShakingSpeed=int(rpm),
                ),
            )
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(
                command,
                HSLHamHeaterShakerLib.StartShaker.Response,
            )

    def get_shaking_speed(self: HamiltonHeaterShaker) -> int:
        command = HSLHamHeaterShakerLib.GetShakerSpeed.Command(
            options=HSLHamHeaterShakerLib.GetShakerSpeed.Options(
                HandleID=self.handle_id,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.GetShakerSpeed.Response,
        )

        return response.ShakerSpeed
