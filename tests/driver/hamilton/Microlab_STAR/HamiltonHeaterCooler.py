import pathlib

from loguru import logger

from plh.device.hamilton_venus import HamiltonHeaterCooler
from plh.device.hamilton_venus.backend import MicrolabSTAR

COM_PORT = "COM7"


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Connect")
    command = HamiltonHeaterCooler.Connect.Command(
        options=HamiltonHeaterCooler.Connect.Options(
            ComPort=COM_PORT,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    handle_id = backend.acknowledge(
        command,
        HamiltonHeaterCooler.Connect.Response,
    ).HandleID

    logger.info("SetTemperature")
    command = HamiltonHeaterCooler.SetTemperature.Command(
        options=HamiltonHeaterCooler.SetTemperature.Options(
            HandleID=handle_id,
            Temperature=60,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, HamiltonHeaterCooler.SetTemperature.Response)

    logger.info("GetTemperature")
    command = HamiltonHeaterCooler.GetTemperature.Command(
        options=HamiltonHeaterCooler.GetTemperature.Options(
            HandleID=handle_id,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HamiltonHeaterCooler.GetTemperature.Response,
        ).Temperature,
    )

    logger.info("StopTemperatureControl")
    command = HamiltonHeaterCooler.StopTemperatureControl.Command(
        options=HamiltonHeaterCooler.StopTemperatureControl.Options(
            HandleID=handle_id,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, HamiltonHeaterCooler.StopTemperatureControl.Response)


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
