from loguru import logger
from plh.driver.HAMILTON import HSLHiGCentrifugeLib
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit

ADAPTER_ID = "HX1"


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Connect")
    command = HSLHiGCentrifugeLib.Connect.Command(
        options=HSLHiGCentrifugeLib.Connect.Options(
            AdapterID=ADAPTER_ID,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLHiGCentrifugeLib.Connect.Response,
    )

    logger.info("Home")
    command = HSLHiGCentrifugeLib.Home.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLHiGCentrifugeLib.Home.Response,
    )

    logger.info("CloseShield")
    command = HSLHiGCentrifugeLib.CloseShield.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLHiGCentrifugeLib.CloseShield.Response,
    )

    logger.info("Spin")
    command = HSLHiGCentrifugeLib.Spin.Command(
        options=HSLHiGCentrifugeLib.Spin.Options(
            GForce=500,
            AccelerationPercent=1,
            DecelerationPercent=1,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLHiGCentrifugeLib.Spin.Response,
    )

    logger.info("IsSpinning")
    command = HSLHiGCentrifugeLib.IsSpinning.Command()
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            HSLHiGCentrifugeLib.IsSpinning.Response,
        ).IsSpinning,
    )

    logger.info("AbortSpin")
    command = HSLHiGCentrifugeLib.AbortSpin.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLHiGCentrifugeLib.AbortSpin.Response,
    )

    logger.info("OpenShield")
    command = HSLHiGCentrifugeLib.OpenShield.Command(
        options=HSLHiGCentrifugeLib.OpenShield.Options(BucketIndex=0),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLHiGCentrifugeLib.OpenShield.Response,
    )

    logger.info("Disconnect")
    command = HSLHiGCentrifugeLib.Disconnect.Command()
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(
        command,
        HSLHiGCentrifugeLib.Disconnect.Response,
    )


if __name__ == "__main__":
    logger.enable("PytomatedLiquidHandling")

    backend = VantageTrackGripperEntryExit(
        identifier="Example Star",
        simulation_on=True,
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
