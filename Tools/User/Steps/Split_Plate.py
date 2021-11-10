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
		if False and Step.GetTitle() == TITLE:
			IsUsedFlag = True
			
			PlateName = Step.GetParentPlate()
			NewPlate1 = Step.GetParameters()[NAME_1]
			NewPlate2 = Step.GetParameters()[NAME_2]
			Factors1 = copy.deepcopy(PLATES.GetPlate(PlateName).GetFactors())
			Factors2 = copy.deepcopy(PLATES.GetPlate(PlateName).GetFactors())
			Choices = SAMPLES.Column(Step.GetParameters()[CHOICE])

			for count in range(0,len(Choices)):
				if Choices[count] == NewPlate1:
					Factors1[count] *= 1
					Factors2[count] *= 0
				elif Choices[count] == NewPlate2:
					Factors1[count] *= 0
					Factors2[count] *= 1
				else:
					Factors1[count] *= 0.5
					Factors2[count] *= 0.5

			PLATES.GetPlate(NewPlate1).SetFactors(Factors1)
			PLATES.GetPlate(NewPlate2).SetFactors(Factors2)

	#for Step in MutableStepsList[:]:
	#	if Step.GetTitle() == PLATE.TITLE:
	#		PLATES.GetPlate(Step.GetParameters()[PLATE.NAME]).SetFactors(PLATES.GetPlate(Step.GetParentPlate()).GetFactors())
	#update all children plates to have the same factor as the parent plate

	#for plate in PLATES.GetDeadPlates():
	#	for Step in MutableStepsList [:]:
	#		if Step.GetParentPlate() == plate:
	#			MutableStepsList.remove(Step)
	#remove plates which have only factors of zero. Otherwise known as dead plates


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
	PLATES.GetPlate(PlateName).SetContext(ParentContext + ":" + ParentPlate)	
	PLATES.GetPlate(PlateName).SetFactors(NewPlate1Factors)

	#create the new plate 1

	PlateName = NewPlate2
	if PLATES.GetPlate(PlateName) == None:
		PLATES.AddPlate(PlateName, NewPlateTypes[PlateName])
		PLATES.GetPlate(PlateName).SetSequences(SAMPLES.GetSequences())
		PLATES.GetPlate(PlateName).SetVolumes([0]*len(SAMPLES.GetSequences()))
	PLATES.GetPlate(PlateName).SetContext(ParentContext + ":" + ParentPlate)	
	PLATES.GetPlate(PlateName).SetFactors(NewPlate2Factors)

	#create new plate 2

	PLATES.GetPlate(ParentPlate).Deactivate()

	DeadPlates = PLATES.GetDeadPlates()

	if NewPlate1 not in DeadPlates:
		PLATES.GetPlate(NewPlate1).Activate()
	
	if NewPlate2 not in DeadPlates:
		PLATES.GetPlate(NewPlate2).Activate()


	LOG.EndCommentsLog()