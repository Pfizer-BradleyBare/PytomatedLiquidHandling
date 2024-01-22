from __future__ import annotations

from dataclasses import field

from pydantic import dataclasses

from plh.driver.HAMILTON import HSLHamHeaterShakerLib
from plh.driver.HAMILTON.backend import HamiltonBackendBase

from .exceptions import CoolingNotSupportedError
from .heat_cool_shake_base import HeatCoolShakeBase, HeatCoolShakeOptions


@dataclasses.dataclass(kw_only=True)
class HamiltonHeaterShaker(HeatCoolShakeBase):
    """Hamilton device that can heat and shake."""

    com_port: int
    """Port to communicate with the device '1'."""

    backend: HamiltonBackendBase
    """This device is only supported by Hamilton backends."""

    handle_id: int = field(init=False, default=0)
    """Handle id used to perform actions after initialization."""

    def assert_options(
        self: HamiltonHeaterShaker,
        options: HeatCoolShakeOptions,
    ) -> None:
        excepts = []

        temperature = options.Temperature

        try:
            super().assert_options(options)
        except ExceptionGroup as e:
            excepts += e.exceptions

        if temperature is not None and temperature < 25:
            excepts.append(CoolingNotSupportedError)

        if len(excepts) > 0:
            msg = "HeatCoolShakeDevice Options Exceptions"
            raise ExceptionGroup(msg, excepts)

    def initialize(self: HamiltonHeaterShaker) -> None:
        """Connects to the Hamilton HeaterShaker then locks and unlocks the plate lock as a reset mechanism."""
        HeatCoolShakeBase.initialize(self)

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
                PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.PlateLockStateOptions.Locked,
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
                PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.PlateLockStateOptions.Unlocked,
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
                PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.PlateLockStateOptions.Unlocked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.SetPlateLock.Response,
        )

        HeatCoolShakeBase.deinitialize(self)

    def set_temperature(
        self: HamiltonHeaterShaker,
        options: HeatCoolShakeOptions,
    ) -> None:
        """Minimum supported temperature is ambient or 25C."""
        self.assert_options(options)

        temperature = options.Temperature

        assert temperature is not None

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
        options: HeatCoolShakeOptions,
    ) -> float:
        self.assert_options(options)
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

    def set_shaking_speed(
        self: HamiltonHeaterShaker,
        options: HeatCoolShakeOptions,
    ) -> None:
        self.assert_options(options)

        rpm = options.RPM

        assert rpm is not None

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
                    PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.PlateLockStateOptions.Unlocked,
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
                    PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.PlateLockStateOptions.Locked,
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
                    ShakingSpeed=rpm,
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
