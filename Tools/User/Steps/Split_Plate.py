from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ...General import Log as LOG
import copy

TITLE = "Split Plate"
CHOICE = "Plate Choice"
NAME_1 = "Plate Name 1"
NAME_2 = "Plate Name 2"

IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			index = MutableStepsList.index(Step)
			MutableStepsList.remove(MutableStepsList[index+2])
			MutableStepsList.remove(MutableStepsList[index+1])
			#Remove the latter step first to prevent list shifting

		#We want to remove the plate actions that follow a split plate. All plate related actions will occur in this action immeditely following a split plate
			

def Step(step):
	LOG.BeginCommentsLog()


	Choices = SAMPLES.Column(step.GetParameters()[CHOICE])
	ParentPlate = step.GetParentPlate()
	NewPlate1 = step.GetParameters()[NAME_1]
	NewPlate2 = step.GetParameters()[NAME_2]
	PLATES.GetPlate(ParentPlate).SetContext(step.GetContext())
	ParentFactors = copy.deepcopy(PLATES.GetPlate(ParentPlate).GetFactors())
	NewPlate1Factors = []
	NewPlate2Factors = []
	#Get step information
			
	for count in range(0,len(Choices)):
		if Choices[count] == NewPlate1:
			NewPlate1Factors.append(1 * ParentFactors[count])
			NewPlate2Factors.append(0 * ParentFactors[count])
		elif Choices[count] == NewPlate2:
			NewPlate1Factors.append(0 * ParentFactors[count])
			NewPlate2Factors.append(1 * ParentFactors[count])
		elif Choices[count] == "Concurrent":
			NewPlate1Factors.append(1 * ParentFactors[count])
			NewPlate2Factors.append(1 * ParentFactors[count])
		#If it is a concurrent workflow then that means we want to maintain the current factors as the parent.
		else:
			NewPlate1Factors.append(0.5 * ParentFactors[count])
			NewPlate2Factors.append(0.5 * ParentFactors[count])
	#Generate the factors for this new plate.


	NewPlateTypes = {}

	AllSteps = STEPS.GetAllSteps()
	for index in range(0,len(AllSteps)):
		if AllSteps[index] == step:
			step1 = AllSteps[index+1]
			step2 = AllSteps[index+2]
			NewPlateTypes[step1.GetParameters()[PLATE.NAME]] = step1.GetParameters()[PLATE.TYPE]
			NewPlateTypes[step2.GetParameters()[PLATE.NAME]] = step2.GetParameters()[PLATE.TYPE]
			break
	#Get type for both new plates

	PlateName = NewPlate1
	if PLATES.GetPlate(PlateName) == None:
		PLATES.AddPlate(PlateName, NewPlateTypes[PlateName])
		PLATES.GetPlate(PlateName).SetSequences(SAMPLES.GetSequences())
		PLATES.GetPlate(PlateName).SetVolumes([0]*len(SAMPLES.GetSequences()))
	PLATES.GetPlate(PlateName).SetContext(step.GetContext() + ":" + PlateName)	
	PLATES.GetPlate(PlateName).SetFactors(NewPlate1Factors)
	#create the new plate 1

	PlateName = NewPlate2
	if PLATES.GetPlate(PlateName) == None:
		PLATES.AddPlate(PlateName, NewPlateTypes[PlateName])
		PLATES.GetPlate(PlateName).SetSequences(SAMPLES.GetSequences())
		PLATES.GetPlate(PlateName).SetVolumes([0]*len(SAMPLES.GetSequences()))
	PLATES.GetPlate(PlateName).SetContext(step.GetContext() + ":" + PlateName)	
	PLATES.GetPlate(PlateName).SetFactors(NewPlate2Factors)
	#create new plate 2

	STEPS.DeactivateContext(step.GetContext())
	STEPS.ActivateContext(step.GetContext() + ":" + NewPlate1)
	STEPS.ActivateContext(step.GetContext() + ":" + NewPlate2)

	LOG.EndCommentsLog()