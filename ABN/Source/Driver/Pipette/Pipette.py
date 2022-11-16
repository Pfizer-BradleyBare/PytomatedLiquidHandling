from .Sequence.SequenceTracker import SequenceTracker
from ...HAL.Pipette import PipetteTracker
from ...API.Workbook import Workbook


def Pipette(
    WorkbookInstance: Workbook,
    SequenceTrackerInstance: SequenceTracker,
    AspiratePipettingDeviceTrackerInstance: PipetteTracker,
    DispensePipettingDeviceTrackerInstance: PipetteTracker,
):

    print("IN PROCESS")

    ContextInstance = WorkbookInstance.GetExecutingContext()

    WellFactorTrackerInstance = ContextInstance.GetWellFactorTracker()
    AspirateWellSequencesTrackerInstance = (
        ContextInstance.GetAspirateWellSequenceTracker()
    )
    DispenseWellSequencesTrackerInstance = (
        ContextInstance.GetDispenseWellSequenceTracker()
    )

    for Sequence in SequenceTrackerInstance.GetObjectsAsList():
        if WellFactorTrackerInstance.GetObjectByName(Sequence.GetName()) == 0:
            continue

        AspirateWellNumber = AspirateWellSequencesTrackerInstance.GetObjectByName(
            Sequence.GetName()
        ).GetSequence()
        DispenseWellNumber = DispenseWellSequencesTrackerInstance.GetObjectByName(
            Sequence.GetName()
        ).GetSequence()

        TransferVolume = Sequence.GetTransferVolume()

        DestinationContainerOperatorInstance = (
            Sequence.GetDestinationContainerOperator()
        )
        SourceContainerOperatorInstance = Sequence.GetSourceContainerOperator()

        DestinationContainerOperatorInstance.Dispense(
            DispenseWellNumber,
            SourceContainerOperatorInstance.Aspirate(
                AspirateWellNumber, TransferVolume
            ),
        )
    # First thing we need to do is update the well volumes. This is going to be something...

    print("COMPLETE")
