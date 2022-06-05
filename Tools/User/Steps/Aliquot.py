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

IsUsedFlag = True

def IsUsed():
	return IsUsedFlag

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	global IsUsedFlag

	NewFactors = [0 for x in PLATES.LABWARE.GetContextualFactors("")]
	#We will start with 0 across the board. Aliquot factors should propagate all the way to the beginning. ALWAYS

	for Step in MutableStepsList[:]:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True

			Params = Step.GetParameters()
			SampleLocations = SAMPLES.Column(Params[LOCATION])

			UniqueSampleLocations = set(SampleLocations)
			#Get unique values by casting to a set

			for UniqueLocation in UniqueSampleLocations:
				NewFactors[int(UniqueLocation) - 1] = SampleLocations.count(UniqueLocation)
			#apply to the factors

			#So I need to adjust factors here.
			#Factor adjustment will ensure enough liquid is available in the wells

	if sum(NewFactors) != 0:
		PLATES.LABWARE.SetContextualFactors("", NewFactors)

def Step(step):
	
	Params = step.GetParameters()
	Source = Params[SOURCE]
	SampleLocations = SAMPLES.Column(Params[LOCATION])
	StartPosition = Params[START]

	
	
	#When the step is run I will adjust the sequences here and readjust the factors.
	#Sequence adjustment will allow me to transfer liquid effectively.
