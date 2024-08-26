import pathlib

from loguru import logger

from plh.device.hamilton_venus import HSLHamHeaterShakerLib
from plh.device.hamilton_venus.backend import MicrolabSTAR

COM_PORT = 1


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("CreateUSBDevice")
    command = HSLHamHeaterShakerLib.CreateUSBDevice.Command(
        options=HSLHamHeaterShakerLib.CreateUSBDevice.Options(
            ComPort=COM_PORT,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    handle_id = backend.acknowledge(
        command,
        HSLHamHeaterShakerLib.CreateUSBDevice.Response,
    ).HandleID

    logger.info("SetPlateLock - Lock")
    command = HSLHamHeaterShakerLib.SetPlateLock.Command(
        options=HSLHamHeaterShakerLib.SetPlateLock.Options(
            HandleID=handle_id,
            PlateLockState=HSLHamHeaterShakerLib.SetPlateLock.LockStateOptions.Locked,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, HSLHamHeaterShakerLib.SetPlateLock.Response)

    logger.info("StartTempCtrl")
    command = HSLHamHeaterShakerLib.StartTempCtrl.Command(
        options=HSLHamHeaterShakerLib.StartTempCtrl.Options(
            HandleID=handle_id,
            Temperature=60,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLHamHeaterShakerLib.StartTempCtrl.Response,
    )

    logger.info("StartShaker")
    command = HSLHamHeaterShakerLib.StartShaker.Command(
        options=HSLHamHeaterShakerLib.StartShaker.Options(
            HandleID=handle_id,
            ShakingSpeed=500,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, HSLHamHeaterShakerLib.StartShaker.Response)

    logger.info("GetTemperature")
    command = HSLHamHeaterShakerLib.GetTemperature.Command(
        options=HSLHamHeaterShakerLib.GetTemperature.Options(
            HandleID=handle_id,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.GetTemperature.Response,
        ).Temperature,
    )

    logger.info("GetShakerSpeed")
    command = HSLHamHeaterShakerLib.GetShakerSpeed.Command(
        options=HSLHamHeaterShakerLib.GetShakerSpeed.Options(
            HandleID=handle_id,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSLHamHeaterShakerLib.GetShakerSpeed.Response,
        ).ShakerSpeed,
    )

    logger.info("StopTempCtrl")
    command = HSLHamHeaterShakerLib.StopTempCtrl.Command(
        options=HSLHamHeaterShakerLib.StopTempCtrl.Options(
            HandleID=handle_id,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, HSLHamHeaterShakerLib.StopTempCtrl.Response)

    logger.info("StopShaker")
    command = HSLHamHeaterShakerLib.StopShaker.Command(
        options=HSLHamHeaterShakerLib.StopShaker.Options(
            HandleID=handle_id,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, HSLHamHeaterShakerLib.StopShaker.Response)


if __name__ == "__main__":
    logger.enable("plh")

    backend = MicrolabSTAR(
        identifier="Example Star",
        simulation_on=True,
        deck_layout=pathlib.Path(__file__).parent / "SimulationLayout.lay",
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
