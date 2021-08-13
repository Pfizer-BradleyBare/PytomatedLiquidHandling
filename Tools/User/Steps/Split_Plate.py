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

			PLATES.GetPlate(NewPlate1).UpdateFactors(Factors1)
			PLATES.GetPlate(NewPlate2).UpdateFactors(Factors2)

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == PLATE.TITLE:
			PLATES.GetPlate(Step.GetParameters()[PLATE.NAME]).UpdateFactors(PLATES.GetPlate(Step.GetParentPlate()).GetFactors())
	#update all children plates to have the same factor as the parent plate

	for plate in PLATES.GetDeadPlates():
		for Step in MutableStepsList [:]:
			if Step.GetParentPlate() == plate:
				MutableStepsList.remove(Step)
	#remove plates which have only factors of zero. Otherwise known as dead plates


def Step(step):
	LOG.Step(step)
	
	PlateName1 = step.GetParameters()[NAME_1]
	PlateName2 = step.GetParameters()[NAME_2]
	PreviousPlateName = step.GetParentPlate()

	PLATES.GetPlate(PreviousPlateName).Deactivate()
	
	DeadPlates = PLATES.GetDeadPlates()

	if PlateName1 not in DeadPlates:
		PLATES.GetPlate(PlateName1).Activate()
	
	if PlateName2 not in DeadPlates:
		PLATES.GetPlate(PlateName2).Activate()