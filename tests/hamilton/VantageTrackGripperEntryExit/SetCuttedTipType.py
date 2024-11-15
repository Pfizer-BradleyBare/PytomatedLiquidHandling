from loguru import logger

from plh.hamilton_venus import SetCuttedTipType
from plh.hamilton_venus.backend import VantageTrackGripperEntryExit


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("SetCuttedTipTypeByLength")
    command = SetCuttedTipType.SetCuttedTipTypeByLength.Command(
        options=SetCuttedTipType.SetCuttedTipTypeByLength.Options(
            TipType=SetCuttedTipType.SetCuttedTipTypeByLength.TipTypeOptions.uL1000,
            CutLength=5,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        SetCuttedTipType.SetCuttedTipTypeByLength.Response,
    )

    logger.info("SetCuttedTipTypeByLength")
    command = SetCuttedTipType.ResetTipType.Command(
        options=SetCuttedTipType.ResetTipType.Options(
            TipType=SetCuttedTipType.ResetTipType.TipTypeOptions.uL1000,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        SetCuttedTipType.ResetTipType.Response,
    )

    logger.info("ResetAllTipTypes")
    command = SetCuttedTipType.ResetAllTipTypes.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        SetCuttedTipType.ResetAllTipTypes.Response,
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
