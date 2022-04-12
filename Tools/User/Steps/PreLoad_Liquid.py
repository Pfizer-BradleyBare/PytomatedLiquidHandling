from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ...User import Samples as SAMPLES
from ...General import Log as LOG

TITLE = "Preload Liquid"
VOLUME = "Volume"


IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList[:]:

		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			
def Step(step):
	DestinationPlate = step.GetParentPlate()
	VolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])

	PlateVolumeList = PLATES.GetPlate(DestinationPlate).GetVolumes()
	PlateFactors = PLATES.GetPlate(DestinationPlate).GetFactors()

	for index in range(0,len(PlateVolumeList)):
		PlateVolumeList[index] -= VolumeList[index] * PlateFactors[index]

	PLATES.GetPlate(DestinationPlate).UpdateMaxVolume()

	for index in range(0,len(PlateVolumeList)):
		PlateVolumeList[index] += (VolumeList[index] + VolumeList[index]) * PlateFactors[index]

	PLATES.GetPlate(DestinationPlate).UpdateMaxVolume()
	#OK what are we doing here? We are subtracting to make the volume is reflected in plate loading.