from .Sequence.SequenceTracker import SequenceTracker
from ...HAL.Pipette import PipetteTracker
from ...HAL.Tools import DeckLoadingItemTracker
from ...API.Tools.Context import Context
from ...API.Workbook.Solution import SolutionTracker


def Pipette(
    SimulateState: bool,
    SequenceTrackerInstance: SequenceTracker,
    SolutionTrackerInstance: SolutionTracker,
    DeckLoadingItemTrackerInstance: DeckLoadingItemTracker,
    ContextInstance: Context,
    AspiratePipettingDeviceTrackerInstance: PipetteTracker,
    DispensePipettingDeviceTrackerInstance: PipetteTracker,
):

    print("IN PROCESS")

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

    if SimulateState is False:
        pass

    print("COMPLETE")
