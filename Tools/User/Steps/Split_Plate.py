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
			#Remove the latter step first to prevent list shifting
		#We want to remove the plate actions that follow a split plate. Why? Because we are going to do the plate work here. It must not be done twice
		# All plate related actions will occur in this action immeditely following a split plate
			

def Step(step):
	Choices = SAMPLES.Column(step.GetParameters()[CHOICE])

	NewPlate1 = step.GetParameters()[NAME_1]
	NewPlate2 = step.GetParameters()[NAME_2]

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


	NextStep = STEPS.GetNextStepInPathway(step)
	NextNextStep = STEPS.GetNextStepInPathway(NextStep)
	#Two Plate Actions will always follow a split plate. ALWAYS
	StepsList = STEPS.GetSteps()
	StepsList.remove(NextNextStep)
	StepsList.remove(NextStep)
	#We are going to remove the Plate Action so the following work is not repeated

	PlateParameters = STEPS.Class.GetParameters(NextStep)
	PlateName = PlateParameters[PLATE.NAME]
	PlateType = PlateParameters[PLATE.TYPE]
	if PLATES.LABWARE.GetLabware(PlateName) == None:
		NewPlate = PLATES.Class(PlateName, PlateType)
		PLATES.LABWARE.AddLabware(NewPlate)

	PLATES.LABWARE.SetContextualFactors(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualFactors(STEPS.Class.GetContext(step)))
	PLATES.LABWARE.SetContextualSequences(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualSequences(STEPS.Class.GetContext(step)))
	#add Plate 1

	PlateParameters = STEPS.Class.GetParameters(NextNextStep)
	PlateName = PlateParameters[PLATE.NAME]
	PlateType = PlateParameters[PLATE.TYPE]
	if PLATES.LABWARE.GetLabware(PlateName) == None:
		NewPlate = PLATES.Class(PlateName, PlateType)
		PLATES.LABWARE.AddLabware(NewPlate)

	PLATES.LABWARE.SetContextualFactors(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualFactors(STEPS.Class.GetContext(step)))
	PLATES.LABWARE.SetContextualSequences(STEPS.Class.GetContext(step) + ":" + PlateName, PLATES.LABWARE.GetContextualSequences(STEPS.Class.GetContext(step)))
	#add Plate 2

	STEPS.DeactivateContext(step.GetContext())
	STEPS.ActivateContext(step.GetContext() + ":" + NewPlate1)
	STEPS.ActivateContext(step.GetContext() + ":" + NewPlate2)