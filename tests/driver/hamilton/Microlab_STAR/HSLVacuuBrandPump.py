import pathlib

from loguru import logger

from plh.driver.HAMILTON import HSLVacuuBrandPump
from plh.driver.HAMILTON.backend import MicrolabSTAR

COM_PORT = 1
PUMP_ID = 1


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Initialize")
    command = HSLVacuuBrandPump.Initialize.Command(
        options=HSLVacuuBrandPump.Initialize.Options(
            ComPort=COM_PORT,
            PumpID=PUMP_ID,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLVacuuBrandPump.Initialize.Response,
    )

    logger.info("ReqActualPressure")
    command = HSLVacuuBrandPump.ReqActualPressure.Command(
        options=HSLVacuuBrandPump.ReqActualPressure.Options(
            PumpID=PUMP_ID,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSLVacuuBrandPump.ReqActualPressure.Response,
        ),
    )

    logger.info("StartPressureControl")
    command = HSLVacuuBrandPump.StartPressureControl.Command(
        options=HSLVacuuBrandPump.StartPressureControl.Options(
            PumpID=PUMP_ID,
            Pressure=600,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLVacuuBrandPump.StartPressureControl.Response,
    )

    logger.info("StopPumpImmediately")
    command = HSLVacuuBrandPump.StopPumpImmediately.Command(
        options=HSLVacuuBrandPump.StopPumpImmediately.Options(
            PumpID=PUMP_ID,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLVacuuBrandPump.StopPumpImmediately.Response,
    )

    logger.info("OpenAirAdmittanceValve")
    command = HSLVacuuBrandPump.OpenAirAdmittanceValve.Command(
        options=HSLVacuuBrandPump.OpenAirAdmittanceValve.Options(
            PumpID=PUMP_ID,
        ),
    )

    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLVacuuBrandPump.OpenAirAdmittanceValve.Response,
    )

    logger.info("Terminate")
    command = HSLVacuuBrandPump.Terminate.Command(
        options=HSLVacuuBrandPump.Terminate.Options(
            PumpID=PUMP_ID,
        ),
    )

    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLVacuuBrandPump.Terminate.Response,
    )


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
