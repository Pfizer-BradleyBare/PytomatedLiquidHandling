import pathlib

from loguru import logger

from plh.driver.HAMILTON import HSL_LiquidClassLib
from plh.driver.HAMILTON.backend import MicrolabSTAR


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing Main() from {__file__}")

    logger.info("TestLiquidClassExists - Pass")
    command = HSL_LiquidClassLib.TestLiquidClassExists.Command(
        options=[
            HSL_LiquidClassLib.TestLiquidClassExists.Options(
                LiquidClass="SlimTipFilter_96COREHead1000ul_Water_DispenseJet_Aliquot",
            ),
        ],
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSL_LiquidClassLib.TestLiquidClassExists.Response,
        ).BadLiquidClasses,
    )

    logger.info("TestLiquidClassExists - Fail")
    command = HSL_LiquidClassLib.TestLiquidClassExists.Command(
        options=[
            HSL_LiquidClassLib.TestLiquidClassExists.Options(
                LiquidClass="Bad Class",
            ),
        ],
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSL_LiquidClassLib.TestLiquidClassExists.Response,
        ).BadLiquidClasses,
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
