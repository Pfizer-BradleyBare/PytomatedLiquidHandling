from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ..Steps import Pool as POOL
from ...User import Samples as SAMPLES
from ...General import Log as LOG
import time

TITLE = "Aliquot"
LOCATION = "Aspirate Location"
START = "Start Position"

IsUsedFlag = False

def IsUsed():
	return IsUsedFlag

def DoesStatusUpdates():
	return False

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	global IsUsedFlag
	IsUsedFlag = True



def Step(step):

	Params = step.GetParameters()
	Start = Params[START]
	AliquotLocations = SAMPLES.Column(Params[LOCATION])

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
	while SearchStep.GetTitle() != POOL.TITLE:
		SearchStep = STEPS.GetPreviousStepInPathway(SearchStep)

		if SearchStep == None:
			MethodComments.append("A Aliquot block must follow a Pool block. There is not a preceeding Pool block. Please Correct")
			break

		if SearchStep.GetTitle() == TITLE:
			MethodComments.append("A Aliquot block cannot come after another Aliquot block. It must be separated by an Pool block. Please Correct")

	if not all(not (type(Location) is str) for Location in AliquotLocations):
		MethodComments.append("The Aspirate Location parameter you provided is not a number. This parameter must be a number. Please Correct")

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
		AliquotLocations = [SAMPLES.GetStartPosition() - 1 + int(Location) for Location in AliquotLocations]
		PLATES.LABWARE.RemoveContextualFlag(Context,"SequenceFromPlateStart")
	else:
		AliquotLocations = [int(Location) for Location in AliquotLocations]
		PLATES.LABWARE.AddContextualFlag(Context,"SequenceFromPlateStart")
	
	PLATES.LABWARE.SetContextualSequences(Context,AliquotLocations)
