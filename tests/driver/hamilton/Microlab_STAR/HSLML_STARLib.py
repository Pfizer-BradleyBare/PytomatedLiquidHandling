import pathlib

from loguru import logger

from plh.device.hamilton_venus import HSLML_STARLib
from plh.device.hamilton_venus.backend import MicrolabSTAR


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("AntiDropletControl_1000uLChannel_On")
    command = HSLML_STARLib.AntiDropletControl_1000uLChannel_On.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLML_STARLib.AntiDropletControl_1000uLChannel_On.Response,
    )

    logger.info("AntiDropletControl_1000uLChannel_Off")
    command = HSLML_STARLib.AntiDropletControl_1000uLChannel_Off.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLML_STARLib.AntiDropletControl_1000uLChannel_Off.Response,
    )

    logger.info("AspirationMonitoring_1000uLChannel_On")
    command = HSLML_STARLib.AspirationMonitoring_1000uLChannel_On.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLML_STARLib.AspirationMonitoring_1000uLChannel_On.Response,
    )

    logger.info("AspirationMonitoring_1000uLChannel_Off")
    command = HSLML_STARLib.AspirationMonitoring_1000uLChannel_Off.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLML_STARLib.AspirationMonitoring_1000uLChannel_Off.Response,
    )

    logger.info("ClotDetectionMonitoring_1000uLChannel_On")
    command = HSLML_STARLib.ClotDetectionMonitoring_1000uLChannel_On.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLML_STARLib.ClotDetectionMonitoring_1000uLChannel_On.Response,
    )

    logger.info("ClotDetectionMonitoring_1000uLChannel_Off")
    command = HSLML_STARLib.ClotDetectionMonitoring_1000uLChannel_Off.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLML_STARLib.ClotDetectionMonitoring_1000uLChannel_Off.Response,
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
