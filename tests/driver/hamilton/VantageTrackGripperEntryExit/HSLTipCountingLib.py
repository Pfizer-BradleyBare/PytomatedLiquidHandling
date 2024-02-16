from loguru import logger

from plh.driver.HAMILTON import HSLTipCountingLib
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Edit - Initial")
    command = HSLTipCountingLib.Edit.Command(
        options=HSLTipCountingLib.Edit.OptionsList(
            TipCounter="Test",
            DialogTitle="Title",
        ),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_1"),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_2"),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_3"),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_4"),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_5"),
    )
    backend.execute(command)
    backend.wait(command)
    available_positions = backend.acknowledge(
        command,
        HSLTipCountingLib.Edit.Response,
    ).AvailablePositions

    logger.info("Write")
    command = HSLTipCountingLib.Write.Command(
        options=HSLTipCountingLib.Write.OptionsList(
            TipCounter="Test",
        ),
    )
    for pos in available_positions:
        command.options.append(
            HSLTipCountingLib.Write.Options(
                LabwareID=pos["LabwareID"],
                PositionID=pos["PositionID"],
            ),
        )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLTipCountingLib.Write.Response,
    )

    logger.info("Edit - Check")
    command = HSLTipCountingLib.Edit.Command(
        options=HSLTipCountingLib.Edit.OptionsList(
            TipCounter="Test",
            DialogTitle="Title",
        ),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_1"),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_2"),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_3"),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_4"),
    )
    command.options.append(
        HSLTipCountingLib.Edit.Options(LabwareID="Tips_FTR_1000uL_5"),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLTipCountingLib.Edit.Response,
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
