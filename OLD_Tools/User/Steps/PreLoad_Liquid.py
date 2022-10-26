from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ..Steps import Plate as PLATE
from ...User import Samples as SAMPLES
from ...General import Log as LOG
from ...General import HamiltonIO as HAMILTONIO

TITLE = "Preload Liquid"
SOURCE = "Source"
VOLUME = "Volume (uL)"

IsUsedFlag = False

def IsUsed():
	return IsUsedFlag

def DoesStatusUpdates():
	return False

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList[:]:

		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			
def Step(step):
	DestinationPlate = step.GetParentPlateName()
	VolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])
	Sources = SAMPLES.Column(step.GetParameters()[SOURCE])

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []

	#Testing Volume
	if not all(not (type(Volume) is str) for Volume in VolumeList):
		MethodComments.append("The Volume parameter you provided is not a number. This parameter must be a number. Please Correct")

	if all(Source != DestinationPlate for Source in Sources):
		MethodComments.append("The Source parameter you provided must be the parent plate. I know it is weird... Please Correct")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)
		if HAMILTONIO.IsSimulated() == True:
			quit()
		else:
			STEPS.UpdateStepParams(step)
			Step(step)
			return

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	SourceLabware = PLATES.LABWARE.GetLabware(DestinationPlate)
	for Source in Sources:
		SourceLabware = PLATES.LABWARE.GetLabware(Source)
		if SourceLabware == None:
			SOLUTIONS.LABWARE.AddLabware(SOLUTIONS.Class(Source))

	Labware = PLATES.LABWARE.GetLabware(DestinationPlate)
	Labware.SetIsPreloaded()
	ContextualString = PLATES.LABWARE.GetContextualStringsList(step,[DestinationPlate])[0]

	PlateVolumeList = Labware.VolumesList
	PlateFactors = PLATES.LABWARE.GetContextualFactors(ContextualString)

	for index in range(0,len(PlateVolumeList)):
		PlateVolumeList[index] -= VolumeList[index] * PlateFactors[index]

	PLATES.Class.DoVolumeUpdate(Labware)

	for index in range(0,len(PlateVolumeList)):
		PlateVolumeList[index] += (VolumeList[index] + VolumeList[index]) * PlateFactors[index]
		Labware.WellContents[index].append({"Solution":Sources[index], "Well":index, "Volume": VolumeList[index]})

	PLATES.Class.DoVolumeUpdate(Labware)
	#OK what are we doing here? We are subtracting to make the volume is reflected in plate loading.