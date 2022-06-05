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
def Init(MutableStepsList):	
	pass

def Step(step):

	PlateName = step.GetParameters()[NAME]
	PlateType = step.GetParameters()[TYPE]
	
	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []

	#Testing Name
	if not type(PlateName) is str:
		MethodComments.append("The Plate Name parameter you provided is a number. This parameter must contain letters. Please Correct")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	if PLATES.LABWARE.GetLabware(PlateName) == None:
		NewPlate = PLATES.Class(PlateName, PlateType)
		PLATES.LABWARE.AddLabware(NewPlate)

	PLATES.LABWARE.SetContextualFactors(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualFactors(STEPS.Class.GetContext(step)))
	PLATES.LABWARE.SetContextualSequences(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualSequences(STEPS.Class.GetContext(step)))
	#Now all the contexts are going to be derived from the parents.

	STEPS.DeactivateContext(step.GetContext())
	STEPS.ActivateContext(step.GetContext()  + ":" + PlateName)