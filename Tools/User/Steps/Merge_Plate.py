from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ..Steps import Wait as WAIT
from ...General import Log as LOG
import copy

TITLE = "Merge Plates"
NAME = "Plate Name"
CONTINUE = "Continue Here?"

IsUsedFlag = False

MergeSteps = []

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True

def Step(step):
	global MergeSteps

	LOG.BeginCommentsLog()

	ParentPlate = step.GetParentPlate()
	WaitingPlate = step.GetParameters()[NAME]
	Continue = step.GetParameters()[CONTINUE]
	#Get step information

	MergeSteps.append(step)
	PLATES.GetPlate(ParentPlate).Deactivate()

	for MergeStep in MergeSteps[:]:
		MergeParent = MergeStep.GetParentPlate()
		MergeWaitingPlate = MergeStep.GetParameters()[NAME]
		MergeContinue = MergeStep.GetParameters()[CONTINUE]

		if MergeWaitingPlate == ParentPlate and MergeParent == WaitingPlate:
			MergeSteps.remove(MergeStep)
			MergeSteps.remove(step)

			if Continue == "Yes" and MergeContinue == "Yes":
				PLATES.GetPlate(ParentPlate).Activate()
				PLATES.GetPlate(MergeParent).Activate()
			else:
				if Continue == "Yes":
					PLATES.GetPlate(ParentPlate).Activate()
				if MergeContinue == "Yes":
					PLATES.GetPlate(MergeParent).Activate()
			#We need ot make sure we restore the factors correctly. If both are yes, then none is actually merged, it is just a pause function.

			return

	WAIT.WaitForTimer()
	#This basically acts as an asynchronous wait function.

	LOG.EndCommentsLog()