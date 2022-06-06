from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ...General import Log as LOG
import copy

TITLE = "Split Plate"
CHOICE = "Plate Choice"
NAME_1 = "Pathway 1"
NAME_2 = "Pathway 2"

IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			

def Step(step):
	Choices = SAMPLES.Column(step.GetParameters()[CHOICE])

	NewPlate1 = step.GetParameters()[NAME_1]
	NewPlate2 = step.GetParameters()[NAME_2]

	NextStep = STEPS.GetNextStepInPathway(step)
	NextNextStep = STEPS.GetNextStepInPathway(NextStep)
	#Two Plate Actions will always follow a split plate. ALWAYS. If not, then the parameters the user entered are wrong.

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []
	
	#Testing NewPlate1
	if not (type(NewPlate1) is str):
		MethodComments.append("The Pathway 1 parameter must contain letters. Please Correct.")
	else:
		TestLabware = PLATES.LABWARE.GetLabware(NewPlate1)
		if TestLabware != None:
			MethodComments.append("Split Plate block pathways must be unqiue. \"" + NewPlate1 + "\" is already a defined plate. Please choose a new name so the plate is unique.")
		
		elif not NextStep.GetTitle() == PLATE.TITLE or not NextNextStep.GetTitle() == PLATE.TITLE or not (NextStep.GetParameters()[PLATE.NAME] == NewPlate1 or NextNextStep.GetParameters()[PLATE.NAME] == NewPlate1):
			MethodComments.append("The Pathway 1 parameter does not match one of the two following Plate blocks. Please ensure the Pathway 1 parameter matches one of the following Plate blocks.")

	#Testing NewPlate2
	if not (type(NewPlate2) is str):
		MethodComments.append("The Pathway 2 parameter must contain letters. Please Correct.")
	else:
		TestLabware = PLATES.LABWARE.GetLabware(NewPlate2)
		if TestLabware != None:
			MethodComments.append("Split Plate block pathways must be unqiue. \"" + NewPlate2 + "\" is already a defined plate. Please choose a new name so the plate is unique.")
		
		elif not NextStep.GetTitle() == PLATE.TITLE or not NextNextStep.GetTitle() == PLATE.TITLE or not (NextStep.GetParameters()[PLATE.NAME] == NewPlate2 or NextNextStep.GetParameters()[PLATE.NAME] == NewPlate2):
			MethodComments.append("The Pathway 2 parameter does not match one of the two following Plate blocks. Please ensure the Pathway 2 parameter matches one of the following Plate blocks.")

	#Testing Choice
	if not all(type(Choice) is str for Choice in Choices):
		MethodComments.append("The Plate Choice parameter must contain letters. Please Correct.")
	
	elif not all(Choice == "Split" or Choice == "Concurrent" or Choice == NewPlate1 or Choice == NewPlate2 for Choice in Choices):
		MethodComments.append("The Plate Choice parameter can be \"Split\", \"Concurrent\", \"" + NewPlate1 + "\", or \"" + NewPlate2 + "\". Please Correct.")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	ContextualFactors = PLATES.LABWARE.GetContextualFactors(STEPS.Class.GetContext(step))

	NewPlate1Factors = []
	NewPlate2Factors = []
	#Get step information
			
	for count in range(0,len(Choices)):
		if Choices[count].lower() == NewPlate1.lower():
			NewPlate1Factors.append(1 * ContextualFactors[count])
			NewPlate2Factors.append(0 * ContextualFactors[count])
		elif Choices[count].lower() == NewPlate2.lower():
			NewPlate1Factors.append(0 * ContextualFactors[count])
			NewPlate2Factors.append(1 * ContextualFactors[count])
		elif Choices[count].lower() == "Concurrent".lower():
			NewPlate1Factors.append(1 * ContextualFactors[count])
			NewPlate2Factors.append(1 * ContextualFactors[count])
		#If it is a concurrent workflow then that means we want to maintain the current factors as the parent.
		elif Choices[count].lower() == "Split".lower():
			NewPlate1Factors.append(0.5 * ContextualFactors[count])
			NewPlate2Factors.append(0.5 * ContextualFactors[count])
		else:
			pass
	#Generate the factors for this new plate.

	PlateParameters = STEPS.Class.GetParameters(NextStep)
	PlateName = PlateParameters[PLATE.NAME]
	PlateType = PlateParameters[PLATE.TYPE]

	NewPlate = PLATES.Class(PlateName, PlateType)
	PLATES.LABWARE.AddLabware(NewPlate)

	PLATES.LABWARE.SetContextualFactors(STEPS.Class.GetContext(step) + ":" + PlateName, NewPlate1Factors)
	PLATES.LABWARE.SetContextualSequences(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualSequences(STEPS.Class.GetContext(step)))
	PLATES.LABWARE.AddContextualFlag(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualFlags(STEPS.Class.GetContext(step)))
	#add Plate 1

	PlateParameters = STEPS.Class.GetParameters(NextNextStep)
	PlateName = PlateParameters[PLATE.NAME]
	PlateType = PlateParameters[PLATE.TYPE]

	NewPlate = PLATES.Class(PlateName, PlateType)
	PLATES.LABWARE.AddLabware(NewPlate)

	PLATES.LABWARE.SetContextualFactors(STEPS.Class.GetContext(step) + ":" + PlateName, NewPlate2Factors)
	PLATES.LABWARE.SetContextualSequences(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualSequences(STEPS.Class.GetContext(step)))
	PLATES.LABWARE.AddContextualFlag(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualFlags(STEPS.Class.GetContext(step)))
	#add Plate 2

	STEPS.DeactivateContext(step.GetContext())
	STEPS.ActivateContext(step.GetContext() + ":" + NewPlate1)
	STEPS.ActivateContext(step.GetContext() + ":" + NewPlate2)