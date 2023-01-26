from ...Driver.Tools.Command.CommandTracker import CommandTracker
from ...Server.Globals.HandlerRegistry import GetAPIHandler
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from .Options.TransferOptionsTracker import TransferOptionsTracker


def Transfer(TransferOptionsTrackerInstance: TransferOptionsTracker):

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

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        GetAPIHandler().LoadedLabwareTrackerInstance  # type:ignore
    )

    DestinationLoadedLabwareInstances = list()
    DestinationLoadedLabwarePhysicalWells = list()
    SourceLoadedLabwareInstances = list()
    SourceLoadedLabwarePhysicalWells = list()

    for TransferOptions in TransferOptionsTrackerInstance.GetObjectsAsList():

        SourceContainerInstance = TransferOptions.SourceContainerInstance
        SourceWellNumber = TransferOptions.SourceWellPosition

        SourceLoadedLabwareTrackerInstance = (
            LoadedLabwareTrackerInstance.GetLabwareAssignments(SourceContainerInstance)
        )

        DestinationContainerInstance = TransferOptions.DestinationContainerInstance
        DestinationWellNumber = TransferOptions.DestinationWellPosition
    # Then we need to convert container wells to loaded labware wells

    # Decide which pipetting device to use based off the source and desitnation labwares

    # Set up the transfer and go
