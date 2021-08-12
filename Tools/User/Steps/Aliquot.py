from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Plate as PLATE
from ...User import Samples as SAMPLES

TITLE = "Aliquot"
NAME = "Source"
LOCATION = "Aspirate Location"
START = "Start Position"


IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

#This function may modify the Mutable list if required
def Init(MutableStepsList):

	PrecedingPlates = set()

	for Step in MutableStepsList[:]:

		if Step.GetTitle() == PLATE.TITLE: 
			PrecedingPlates.add(Step.GetParameters()[PLATE.NAME])

		if Step.GetTitle() == TITLE:
			PrecedingPlates.add(Step.GetParameters()[NAME])
			PrecedingPlates.remove(Step.GetParentPlate())

			LocationsList = SAMPLES.Column(Step.GetParameters()[LOCATION])
			SampleLocationsList = []
			PlateLocationsList = []
			
			for Location in LocationsList:
				SampleLocationsList.append(int(Location) + SAMPLES.GetStartPosition() - 1)
				PlateLocationsList.append(int(Location))

			for PlateName in PrecedingPlates:
				Plate = PLATES.GetPlate(PlateName)

				Factors = Plate.GetFactors()
				Sequences = Plate.GetSequenceList()

				Indices = []

				for Location in SampleLocationsList:
					for SequenceList in Sequences:
						for Sequence in SequenceList:
							if Location == Sequence:
								Indices.append(Sequences.index(SequenceList))
				#Get sequence index for location 

				NewFactors = []
				NewSequences = []

				for Index in Indices:
					NewFactors.append(Factors[Index])
					Multiplier = len(Sequences[Index])
					if Step.GetParameters()[START] == "Sample Start Position":
						NewSequences.append([SampleLocationsList[Index]*Multiplier])
					else:
						NewSequences.append([PlateLocationsList[Index]*Multiplier])

				Plate.UpdateFactors(NewFactors)
				Plate.UpdateSequenceList(NewSequences)

			PrecedingPlates = set()
			#Reset the preceding plates

def Step(step):
	pass