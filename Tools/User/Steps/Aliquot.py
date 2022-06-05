from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ..Steps import Split_Plate as SPLIT_PLATE
from ...User import Samples as SAMPLES
from ...General import Log as LOG
import time

TITLE = "Aliquot"
SOURCE = "Source"
LOCATION = "Aspirate Location"
START = "Start Position"

IsUsedFlag = False

def IsUsed():
	return IsUsedFlag

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	global IsUsedFlag

	AliquotStepCount = 0

	NewFactors = [0 for x in PLATES.LABWARE.GetContextualFactors("")]
	#We will start with 0 across the board. Aliquot factors should propagate all the way to the beginning. ALWAYS

	SplitPlateFound = False

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == SPLIT_PLATE.TITLE:
			SplitPlateFound = True
		
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True

			Params = Step.GetParameters()
			SampleLocations = SAMPLES.Column(Params[LOCATION])

			#########################
			#########################
			#########################
			#### INPUT VALIDATION ###
			#########################
			#########################
			#########################
			MethodComments = []

			AliquotStepCount += 1
			if AliquotStepCount > 1:
				MethodComments.append("Only one Aliquot block is allowed in a method. Pleae Correct.")

			if SplitPlateFound == True:
				MethodComments.append("An Aliquot block can not follow a Split Plate block. Pleae Correct.")

			#Testing Sample Locations
			if not all(not (type(Location) is str) for Location in SampleLocations):
				MethodComments.append("The Aspirate Location parameter you provided is not a number. This parameter must be a number. Please Correct")

			if len(MethodComments) != 0:
				LOG.LogMethodComment(Step,MethodComments)

			#########################
			#########################
			#########################
			#### INPUT VALIDATION ###
			#########################
			#########################
			#########################

			UniqueSampleLocations = set(SampleLocations)
			#Get unique values by casting to a set

			for UniqueLocation in UniqueSampleLocations:
				NewFactors[int(UniqueLocation) - 1] = SampleLocations.count(UniqueLocation)
			#apply to the factors

			#So I need to adjust factors here.
			#Factor adjustment will ensure enough liquid is available in the wells

	if IsUsedFlag == True:
		PLATES.LABWARE.SetContextualFactors("", NewFactors)
	
def Step(step):
	
	Params = step.GetParameters()
	Source = Params[SOURCE]
	SampleLocations = SAMPLES.Column(Params[LOCATION])
	StartPosition = Params[START]

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []
	
	#Testing Source
	if not (type(Source) is str):
		MethodComments.append("The Source parameter you provided is a number. This parameter must contain letters. Please Correct")
	else:
		TestLabware = PLATES.LABWARE.GetLabware(Source)
		if TestLabware == None:
			MethodComments.append("The Source parameter you provided is a solution. Only a plate name is acceptable. Please correct.")
		else:
			if TestLabware.GetLabwareType() == PLATES.LABWARE.LabwareTypes.Reagent:
				MethodComments.append("The Source parameter you provided is a solution. Only a plate name is acceptable. Please correct.")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################


	#we need to go back and find the Source plate block
	SearchStep = step
	SourceContext = ""
	while SearchStep.GetTitle() != PLATE.TITLE or SearchStep.GetParameters()[PLATE.NAME] != Source:
		
		if SearchStep.GetTitle() == PLATE.TITLE:
			SourceContext = SearchStep.GetContext()

		SearchStep = STEPS.GetPreviousStepInPathway(SearchStep)

		if SearchStep == None:
			break

	PLATES.LABWARE.SetContextualFactors(step.GetContext(),PLATES.LABWARE.GetDefaultFactors())
	
	if StartPosition == "Sample Start Position":
		Sequence = [SAMPLES.GetStartPosition() - 1 + int(Location) for Location in SampleLocations]
	else:
		Sequence = [int(Location) for Location in SampleLocations]
		PLATES.LABWARE.GetLabware(Source).SetIsModifierAliquot()

	PLATES.LABWARE.SetContextualSequences(SourceContext,Sequence)


	#When the step is run I will adjust the sequences here and readjust the factors.
	#Sequence adjustment will allow me to transfer liquid effectively.
