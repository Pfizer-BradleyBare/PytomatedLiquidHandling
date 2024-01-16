from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, Literal

from pydantic import dataclasses

from plh.driver.HAMILTON import HSLHamHeaterShakerLib

from .exceptions import CoolingNotSupportedError
from .heat_cool_shake_base import HeatCoolShakeBase

if TYPE_CHECKING:
    from plh.driver.HAMILTON.backend import HamiltonBackendBase
    from plh.hal import layout_item as li


@dataclasses.dataclass(kw_only=True)
class HamiltonHeaterShaker(HeatCoolShakeBase):
    com_port: int
    backend: HamiltonBackendBase
    backend_error_handling: Literal["N/A"] = "N/A"
    handle_id: int = field(init=False)

    def assert_options(
        self: HamiltonHeaterShaker,
        layout_item: li.LayoutItemBase,
        temperature: float | None = None,
        rpm: int | None = None,
    ) -> None:
        excepts = []

        try:
            super().assert_options(layout_item, temperature, rpm)
        except ExceptionGroup as e:
            excepts += e.exceptions

        if temperature is not None and temperature < 25:
            excepts.append(CoolingNotSupportedError)

        if len(excepts) > 0:
            msg = "HeatCoolShakeDevice Options Exceptions"
            raise ExceptionGroup(msg, excepts)

    def initialize(self: HamiltonHeaterShaker) -> None:
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
                HandleID=int(self.handle_id),
                PlateLockState=1,
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
                HandleID=int(self.handle_id),
                PlateLockState=0,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.SetPlateLock.Response,
        )

    def deinitialize(self: HamiltonHeaterShaker) -> None:
        command = HSLHamHeaterShakerLib.StopTempCtrl.Command(
            options=HSLHamHeaterShakerLib.StopTempCtrl.Options(
                HandleID=int(self.handle_id),
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
                HandleID=int(self.handle_id),
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
                HandleID=int(self.handle_id),
                PlateLockState=0,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.SetPlateLock.Response,
        )

        HeatCoolShakeBase.deinitialize(self)

    def set_temperature(self: HamiltonHeaterShaker, temperature: float) -> None:
        if temperature < 25:
            raise CoolingNotSupportedError

        command = HSLHamHeaterShakerLib.StartTempCtrl.Command(
            options=HSLHamHeaterShakerLib.StartTempCtrl.Options(
                HandleID=int(self.handle_id),
                Temperature=temperature,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.StartTempCtrl.Response,
        )

    def time_to_temperature(self: HamiltonHeaterShaker, temperature: float) -> float:
        return 0

    def get_temperature(self: HamiltonHeaterShaker) -> float:
        command = HSLHamHeaterShakerLib.GetTemperature.Command(
            options=HSLHamHeaterShakerLib.GetTemperature.Options(
                HandleID=int(self.handle_id),
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.GetTemperature.Response,
        )

        return response.Temperature

    def set_shaking_speed(self: HamiltonHeaterShaker, rpm: int) -> None:
        if rpm == 0:
            command = HSLHamHeaterShakerLib.StopShaker.Command(
                options=HSLHamHeaterShakerLib.StopShaker.Options(
                    HandleID=int(self.handle_id),
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
                    HandleID=int(self.handle_id),
                    PlateLockState=0,
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
                    HandleID=int(self.handle_id),
                    PlateLockState=1,
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
                    HandleID=int(self.handle_id),
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
                HandleID=int(self.handle_id),
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        response = self.backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.GetShakerSpeed.Response,
        )

        return response.ShakerSpeed
