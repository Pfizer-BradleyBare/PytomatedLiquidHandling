from loguru import logger

from plh.hamilton_venus.backend import VantageTrackGripperEntryExit
from plh.hamilton_venus.ML_STAR import Channel1000uLCOREGrip


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("GetPlate")
    command = Channel1000uLCOREGrip.GetPlate.Command(
        options=Channel1000uLCOREGrip.GetPlate.Options(
            GripperLabwareID="CORE_Grip_Tool",
            PlateLabwareID="Plate_1",
            GripWidth=87,
            OpenWidth=91,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Channel1000uLCOREGrip.GetPlate.Response)

    logger.info("PlacePlate")
    command = Channel1000uLCOREGrip.PlacePlate.Command(
        options=Channel1000uLCOREGrip.PlacePlate.Options(
            LabwareID="Plate_1",
            EjectTool=True,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Channel1000uLCOREGrip.PlacePlate.Response)


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
