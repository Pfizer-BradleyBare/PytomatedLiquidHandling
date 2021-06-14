from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Split_Plate as SPLIT_PLATE

TITLE = "Plate"
NAME = "Name"
TYPE = "Type"

#This function may modify the Mutable list if required
def Init(MutableStepsList, SequencesList):
	for Step in MutableStepsList[:]:
		if Step.GetTitle() == TITLE:
			PLATES.AddPlate(Step.GetParameters()[NAME], Step.GetParameters()[TYPE], SequencesList)
			if Step.GetParentPlate() == None:
				MutableStepsList.remove(Step)

def Step(step):
	PlateName = step.GetParameters()[NAME]
	PreviousPlateName = step.GetParentPlate()

	PLATES.GetPlate(PreviousPlateName).Deactivate()
	PLATES.GetPlate(PlateName).Activate()