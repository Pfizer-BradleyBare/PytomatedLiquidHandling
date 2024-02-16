import pathlib

from loguru import logger

from plh.driver.HAMILTON import Visual_NTR_Library
from plh.driver.HAMILTON.backend import MicrolabSTAR


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Channels_TipCounter_Edit - Initial")
    command = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
        options=Visual_NTR_Library.Channels_TipCounter_Edit.OptionsList(
            TipCounter="Test",
            DialogTitle="Title",
        ),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_1_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_1_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_1_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_1_0004"),
    )

    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_2_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_2_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_2_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_2_0004"),
    )

    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_3_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_3_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_3_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_3_0004"),
    )

    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_4_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_4_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_4_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_4_0004"),
    )

    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_5_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_5_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_5_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_5_0004"),
    )

    backend.execute(command)
    backend.wait(command)
    available_positions = backend.acknowledge(
        command,
        Visual_NTR_Library.Channels_TipCounter_Edit.Response,
    ).AvailablePositions

    logger.info(available_positions)

    logger.info("Channels_TipCounter_Write")
    command = Visual_NTR_Library.Channels_TipCounter_Write.Command(
        options=Visual_NTR_Library.Channels_TipCounter_Write.OptionsList(
            TipCounter="Test",
        ),
    )
    for pos in available_positions:
        command.options.append(
            Visual_NTR_Library.Channels_TipCounter_Write.Options(
                LabwareID=pos["LabwareID"],
                PositionID=pos["PositionID"],
            ),
        )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        Visual_NTR_Library.Channels_TipCounter_Write.Response,
    )

    logger.info("Channels_TipCounter_Edit - Check")
    command = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
        options=Visual_NTR_Library.Channels_TipCounter_Edit.OptionsList(
            TipCounter="Test",
            DialogTitle="Title",
        ),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_1_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_1_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_1_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_1_0004"),
    )

    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_2_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_2_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_2_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_2_0004"),
    )

    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_3_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_3_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_3_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_3_0004"),
    )

    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_4_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_4_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_4_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_4_0004"),
    )

    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_5_0001"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_5_0002"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_5_0003"),
    )
    command.options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID="NTR_5_0004"),
    )

    backend.execute(command)
    backend.wait(command)
    available_positions = backend.acknowledge(
        command,
        Visual_NTR_Library.Channels_TipCounter_Edit.Response,
    ).AvailablePositions


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
