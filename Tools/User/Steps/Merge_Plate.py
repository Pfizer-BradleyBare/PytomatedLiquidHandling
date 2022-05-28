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

	ParentPlate = step.GetParentPlateName()
	Context = step.GetContext()
	WaitingPlate = step.GetParameters()[NAME]
	Continue = step.GetParameters()[CONTINUE]
	#Get step information

	for MergeStep in MergeSteps[:]:
		MergeParent = MergeStep.GetParentPlateName()
		MergeContext = MergeStep.GetContext()
		MergeWaitingPlate = MergeStep.GetParameters()[NAME]
		MergeContinue = MergeStep.GetParameters()[CONTINUE]

		if MergeWaitingPlate == ParentPlate and MergeParent == WaitingPlate:
			MergeSteps.remove(MergeStep)

			if Continue == "Yes" and MergeContinue == "Yes":
				STEPS.ActivateContext(Context)
				STEPS.ActivateContext(MergeContext)
			else:
				if Continue == "Yes":
					STEPS.ActivateContext(Context)
				if MergeContinue == "Yes":
					STEPS.ActivateContext(MergeContext)
			#We need ot make sure we restore the factors correctly. If both are yes, then none is actually merged, it is just a pause function.

			return

	MergeSteps.append(step)
	STEPS.DeactivateContext(Context)

	WAIT.WaitForTimer()
	#This basically acts as an asynchronous wait function.