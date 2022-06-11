from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Split_Plate as SPLIT_PLATE
from ..Steps import Aliquot as ALIQUOT
from ...General import Log as LOG
from ...User import Samples as SAMPLES

TITLE = "Pool"
LOCATION = "Dispense Location"
START = "Start Position"

IsUsedFlag = True

def IsUsed():
	return IsUsedFlag

def DoesStatusUpdates():
	return False

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	pass

def Step(step):
	
	Params = step.GetParameters()
	Start = Params[START]
	PoolLocations = SAMPLES.Column(Params[LOCATION])

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []

	#we need to go back and find the preceding pool block
	SearchStep = step
	while SearchStep.GetTitle() != ALIQUOT.TITLE:
		SearchStep = STEPS.GetPreviousStepInPathway(SearchStep)

		if SearchStep == None:
			break

		if SearchStep.GetTitle() == TITLE:
			MethodComments.append("A Pool block cannot come after another Pool block. It must be separated by an Alqiuot block. Please Correct")	

	if not all(not (type(Location) is str) for Location in PoolLocations):
		MethodComments.append("The Dispense Location parameter you provided is not a number. This parameter must be a number. Please Correct")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	Context = step.GetContext()

	if Start == "Sample Start Position":
		PoolLocations = [SAMPLES.GetStartPosition() - 1 + int(Location) for Location in PoolLocations]
		PLATES.LABWARE.RemoveContextualFlag(Context,"SequenceFromPlateStart")
	else:
		PoolLocations = [int(Location) for Location in PoolLocations]
		PLATES.LABWARE.AddContextualFlag(Context,"SequenceFromPlateStart")

	PLATES.LABWARE.SetContextualSequences(Context,PoolLocations)
	#Very simple. Just change the sequences and now everything will be pooled!!