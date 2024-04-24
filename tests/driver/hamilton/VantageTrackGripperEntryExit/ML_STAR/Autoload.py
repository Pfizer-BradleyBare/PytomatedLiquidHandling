from loguru import logger

from plh.device.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.device.HAMILTON.ML_STAR import Autoload


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("MoveAutoLoad")
    command = Autoload.MoveAutoLoad.Command(
        options=Autoload.MoveAutoLoad.Options(
            TrackNumber=40,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Autoload.MoveAutoLoad.Response)

    logger.info("UnloadCarrier")
    command = Autoload.UnloadCarrier.Command(
        options=Autoload.UnloadCarrier.Options(
            LabwareID="PLT_CAR_L5AC_A00_0001",
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Autoload.UnloadCarrier.Response)

    logger.info("LoadCarrier")
    command = Autoload.LoadCarrier.Command(
        options=Autoload.LoadCarrier.Options(
            LabwareID="PLT_CAR_L5AC_A00_0001",
            LabwarePositions=Autoload.LoadCarrier.LabwarePositionsOptions.ReadPresentLabware,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Autoload.LoadCarrier.Response)


if __name__ == "__main__":
    logger.enable("plh")

    backend = VantageTrackGripperEntryExit(
        identifier="Example Star",
        simulation_on=True,
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
