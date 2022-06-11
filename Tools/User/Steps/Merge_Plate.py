from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ..Steps import Split_Plate as SPLIT_PLATE
from ..Steps import Wait as WAIT
from ...General import Log as LOG
import copy

TITLE = "Merge Plates"
NAME = "Plate Name"
CONTINUE = "Continue Here?"

IsUsedFlag = False

MergeSteps = []
MergedPathways = set()

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def DoesStatusUpdates():
	return False

def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True

def Step(step):
	global MergeSteps

	SearchStep = step
	PlateStep = step
	PreviousContext = ""

	while SearchStep.GetTitle() != SPLIT_PLATE.TITLE and not (str(SearchStep.GetCoordinates()) in MergedPathways):
		
		if SearchStep.GetTitle() != PLATE.TITLE:
			PreviousContext = SearchStep.GetContext()

		if SearchStep.GetTitle() == PLATE.TITLE and SearchStep.GetContext()+":"+SearchStep.GetParameters()[PLATE.NAME] in PreviousContext:
			PlateStep = SearchStep

		SearchStep = STEPS.GetPreviousStepInPathway(SearchStep)

		if SearchStep == None:
			break
	#We need to find the preceeding split plate step and the parent of the entire pathway. Easy two birds

	ParentPlate = step.GetParentPlateName()
	Context = step.GetContext()
	WaitingPlate = step.GetParameters()[NAME]
	Continue = step.GetParameters()[CONTINUE]
	#Get step information

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []

	if SearchStep == None:
		MethodComments.append("A Merge Plates block can only come after a split plates step. Please Correct.")
	else:
		Params = SearchStep.GetParameters()
		MergePlateOptions = [Params[SPLIT_PLATE.NAME_1], Params[SPLIT_PLATE.NAME_2]]
		CorrectParent = PlateStep.GetParameters()[PLATE.NAME]

		if not (ParentPlate == CorrectParent):
			MethodComments.append("You must merge with the same parent plate that started this new pathway. Correct Parent is \"" + CorrectParent + "\". Please reactivate the correct parent plate.")

		MergePlateOptions.remove(CorrectParent)
		CorrectMergePlate = MergePlateOptions[0]

		if not (WaitingPlate == CorrectMergePlate):
			MethodComments.append("The Plate Name parameter must be the other pathways parent plate. Correct Plate Name is \"" + CorrectMergePlate + "\". Please Correct.")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	STEPS.DeactivateContext(Context)

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
			#This is functionally a synchronization step. So we do not consider the pathway merged yet.
			else:
				MergedPathways.add(str(SearchStep.GetCoordinates()))
				#This pathway is now merged!

				UpdateFactorsFlag = False
				if SearchStep.GetParameters()[SPLIT_PLATE.CHOICE] != "Split" and SearchStep.GetParameters()[SPLIT_PLATE.CHOICE] != "Concurrent":
					UpdateFactorsFlag = True
				#I don't want to update the factors if it is split or concurrent. This would make the factors larger than the volume present in the wells.

				Factors = PLATES.LABWARE.GetContextualFactors(Context)
				MergeFactors = PLATES.LABWARE.GetContextualFactors(MergeContext)
				NewFactors = [a + b for a,b in zip(Factors,MergeFactors)]

				if Continue == "Yes":
					if UpdateFactorsFlag == True:
						PLATES.LABWARE.SetContextualFactors(Context, NewFactors)
					STEPS.ActivateContext(Context)

				if MergeContinue == "Yes":
					if UpdateFactorsFlag == True:
						PLATES.LABWARE.SetContextualFactors(MergeContext, NewFactors)
					STEPS.ActivateContext(MergeContext)
			return

	MergeSteps.append(step)

	WAIT.WaitForTimer()
	#This basically acts as an asynchronous wait function.