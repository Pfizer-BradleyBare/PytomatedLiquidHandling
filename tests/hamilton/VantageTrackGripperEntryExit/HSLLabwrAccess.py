from loguru import logger

from plh.hamilton_venus import HSLLabwrAccess
from plh.hamilton_venus.backend import VantageTrackGripperEntryExit


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("AbsolutePositionValuesGetForLabwareID")
    command = HSLLabwrAccess.AbsolutePositionValuesGetForLabwareID.Command(
        options=[
            HSLLabwrAccess.AbsolutePositionValuesGetForLabwareID.Options(
                LabwareID="Ham_24_RB_TuR_1_5ml_0001",
            ),
        ],
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSLLabwrAccess.AbsolutePositionValuesGetForLabwareID.Response,
        ).LabwarePositions,
    )

    logger.info("AbsolutePositionValuesGetForLabwareID")
    command = HSLLabwrAccess.AbsolutePositionValuesSetForLabwareID.Command(
        options=[
            HSLLabwrAccess.AbsolutePositionValuesSetForLabwareID.Options(
                LabwareID="Ham_24_RB_TuR_1_5ml_0001",
                XPosition=0,
                YPosition=0,
                ZPosition=0,
                ZRotation=0,
            ),
        ],
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLLabwrAccess.AbsolutePositionValuesSetForLabwareID.Response,
    )

    logger.info("ValueForKeySetForPropertiesOfLabwareID")
    command = HSLLabwrAccess.ValueForKeySetForPropertiesOfLabwareID.Command(
        options=HSLLabwrAccess.ValueForKeySetForPropertiesOfLabwareID.OptionsList(
            PropertyKey="Test",
            PropertyValue="T",
        ),
    )
    command.options.append(
        HSLLabwrAccess.ValueForKeySetForPropertiesOfLabwareID.Options(
            LabwareID="Ham_24_RB_TuR_1_5ml_0001",
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLLabwrAccess.AbsolutePositionValuesSetForLabwareID.Response,
    )

    logger.info("TestLabwareIDExists - Pass")
    command = HSLLabwrAccess.TestLabwareIDExists.Command(
        options=[
            HSLLabwrAccess.TestLabwareIDExists.Options(
                LabwareID="Ham_24_RB_TuR_1_5ml_0001",
            ),
        ],
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSLLabwrAccess.TestLabwareIDExists.Response,
        ).BadLabwareIDs,
    )

    logger.info("TestLabwareIDExists - Fail")
    command = HSLLabwrAccess.TestLabwareIDExists.Command(
        options=[
            HSLLabwrAccess.TestLabwareIDExists.Options(
                LabwareID="Bad Labware",
            ),
        ],
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSLLabwrAccess.TestLabwareIDExists.Response,
        ).BadLabwareIDs,
    )


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
