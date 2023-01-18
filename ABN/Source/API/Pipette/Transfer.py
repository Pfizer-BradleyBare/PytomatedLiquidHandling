from ...Driver.Tools.Command.CommandTracker import CommandTracker
from .Options.TransferOptionsTracker import TransferOptionsTracker


def Transfer(TransferOptionsTrackerInstance: TransferOptionsTracker) -> CommandTracker:
    ...

    for TransferOptions in TransferOptionsTrackerInstance.GetObjectsAsList():
        Volume = TransferOptions.TransferVolume
        SourceContainerInstance = TransferOptions.SourceContainerInstance
        SourceWellNumber = TransferOptions.SourceWellPosition
        DestinationContainerInstance = TransferOptions.DestinationContainerInstance
        DestinationWellNumber = TransferOptions.DestinationWellPosition

        DestinationContainerInstance.Dispense(
            DestinationWellNumber,
            SourceContainerInstance.Aspirate(SourceWellNumber, Volume),
        )
        # First we do the "programmatic" transfer

    # Then we need to convert container wells to loaded labware wells

    # Decide which pipetting device to use based off the source and desitnation labwares

    # Set up the transfer and go
