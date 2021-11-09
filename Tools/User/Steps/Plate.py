from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Split_Plate as SPLIT_PLATE
from ...User import Samples as SAMPLES
from ...General import Log as LOG

TITLE = "Plate"
NAME = "Name"
TYPE = "Type"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

#This function may modify the Mutable list if required
def Init(MutableStepsList, SequencesList):
	step = MutableStepsList.pop(0)

	PlateName = step.GetParameters()[NAME]
	PLATES.AddPlate(PlateName, step.GetParameters()[TYPE])
	PLATES.GetPlate(PlateName).SetSequences(SAMPLES.GetSequences())
	PLATES.GetPlate(PlateName).SetContext(PlateName)	
	PLATES.GetPlate(PlateName).SetFactors([1]*len(SAMPLES.GetSequences()))
	PLATES.GetPlate(PlateName).SetVolumes([0]*len(SAMPLES.GetSequences()))

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == TITLE:
			if Step.GetParentPlate() == None:
				MutableStepsList.remove(Step)
	#Remove steps following a split plate.


def Step(step):
	LOG.BeginCommentsLog()

	PlateName = step.GetParameters()[NAME]
	PlateType = step.GetParameters()[TYPE]
	ParentPlate = step.GetParentPlate()
	ParentContext = PLATES.GetPlate(ParentPlate).GetContext()
	ParentFactors = PLATES.GetPlate(ParentPlate).GetFactors()

	print(ParentContext + ":" + ParentPlate)
	PLATES.AddPlate(step.GetParameters()[NAME], step.GetParameters()[TYPE])
	PLATES.GetPlate(PlateName).SetSequences(SAMPLES.GetSequences())
	PLATES.GetPlate(PlateName).SetContext(ParentContext + ":" + ParentPlate)	
	PLATES.GetPlate(PlateName).SetFactors(ParentFactors)
	PLATES.GetPlate(PlateName).SetVolumes([0]*len(SAMPLES.GetSequences()))

	PLATES.GetPlate(ParentPlate).Deactivate()
	PLATES.GetPlate(PlateName).Activate()
	
	LOG.EndCommentsLog()