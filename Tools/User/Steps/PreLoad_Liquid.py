from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ...User import Samples as SAMPLES
from ...General import Log as LOG

TITLE = "Preload Liquid"
VOLUME = "Volume (uL)"

IsUsedFlag = False

def IsUsed():
	return IsUsedFlag

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList[:]:

		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			
def Step(step):
	DestinationPlate = step.GetParentPlateName()
	VolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])

	Labware = PLATES.LABWARE.GetLabware(DestinationPlate)
	ContextualString = PLATES.LABWARE.GetContextualStringsList(step,[DestinationPlate])[0]

	PlateVolumeList = Labware.VolumesList
	PlateFactors = PLATES.LABWARE.GetContextualFactors(ContextualString)

	for index in range(0,len(PlateVolumeList)):
		PlateVolumeList[index] -= VolumeList[index] * PlateFactors[index]

	PLATES.Class.DoVolumeUpdate(Labware)

	for index in range(0,len(PlateVolumeList)):
		PlateVolumeList[index] += (VolumeList[index] + VolumeList[index]) * PlateFactors[index]

	PLATES.Class.DoVolumeUpdate(Labware)
	#OK what are we doing here? We are subtracting to make the volume is reflected in plate loading.