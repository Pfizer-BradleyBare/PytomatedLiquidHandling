import pathlib

from loguru import logger

from plh.driver.HAMILTON import HSLTipCountingLib
from plh.driver.HAMILTON.backend import MicrolabSTAR


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing Main() from {__file__}")

    logger.info("Edit - Initial")
    command = HSLTipCountingLib.Edit.Command(
        options=HSLTipCountingLib.Edit.OptionsList(
            TipCounter="Test",
            DialogTitle="Title",
        ),
    )
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_1"))
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_2"))
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_3"))
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_4"))
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_5"))
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
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_1"))
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_2"))
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_3"))
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_4"))
    command.options.append(HSLTipCountingLib.Edit.Options(LabwareID="FTR_5"))
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLTipCountingLib.Edit.Response,
    )


if __name__ == "__main__":
    logger.enable("PytomatedLiquidHandling")

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