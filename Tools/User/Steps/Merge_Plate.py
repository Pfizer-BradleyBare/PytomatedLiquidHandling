from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ...General import Log as LOG
import copy

TITLE = "Merge Plate"
NAME = "Plate Name"

IsUsedFlag = False

MergedPlates = {}

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True



		#We want to ensure we wait for all plates before we start on a merge pathway
			

def Step(step):
	LOG.BeginCommentsLog()


	Choices = SAMPLES.Column(step.GetParameters()[CHOICE])
	ParentPlate = step.GetParentPlate()
	NewPlate1 = step.GetParameters()[NAME_1]
	NewPlate2 = step.GetParameters()[NAME_2]
	ParentFactors = copy.deepcopy(PLATES.GetPlate(ParentPlate).GetFactors())
	ParentContext = PLATES.GetPlate(ParentPlate).GetContext()
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
	PLATES.GetPlate(PlateName).SetContext(step,PlateName)	
	PLATES.GetPlate(PlateName).SetFactors(NewPlate1Factors)
	#create the new plate 1

	PlateName = NewPlate2
	if PLATES.GetPlate(PlateName) == None:
		PLATES.AddPlate(PlateName, NewPlateTypes[PlateName])
		PLATES.GetPlate(PlateName).SetSequences(SAMPLES.GetSequences())
		PLATES.GetPlate(PlateName).SetVolumes([0]*len(SAMPLES.GetSequences()))
	PLATES.GetPlate(PlateName).SetContext(step,PlateName)	
	PLATES.GetPlate(PlateName).SetFactors(NewPlate2Factors)
	#create new plate 2

	PLATES.GetPlate(ParentPlate).Deactivate()

	DeadPlates = PLATES.GetDeadPlates()

	if NewPlate1 not in DeadPlates:
		PLATES.GetPlate(NewPlate1).Activate()
	
	if NewPlate2 not in DeadPlates:
		PLATES.GetPlate(NewPlate2).Activate()


	LOG.EndCommentsLog()