from ..Steps import Steps as STEPS
from ..Steps import Incubate as INCUBATE
from ..Labware import Solutions as SOLUTIONS
from ..Labware import Plates as PLATES
from ...User import Samples as SAMPLES
from ...User import Configuration as CONFIGURATION
from ...Hamilton.Commands import Desalt as DESALT

TITLE = "Desalt"
SOURCE = "Source"
EQUILIBRATION_BUFFER = "Equilibration Buffer"
VOLUME = "Sample Volume (uL)"

#This variable tracks whether or not the tips have been equilibrated
Equilibrated = None
Sample_Volume = 0
Sample_Source = None
Equilibration_Buffer = None
Destination = None
Incubation_Equilibration_Step = None

def GetEquilibrationStep():
	global Incubation_Equilibration_Step
	return Incubation_Equilibration_Step

def Init(MutableStepsList):
	global Equilibrated
	global Incubation_Equilibration_Step
	global Sample_Volume
	global Sample_Source
	global Equilibration_Buffer
	global Destination
	
	Equilibrated = False
	Latest_Incubate_Step = None

	for Step in MutableStepsList:
		if Step.GetTitle() == INCUBATE.TITLE:
			Latest_Incubate_Step = Step

		if Step.GetTitle() == TITLE:
			
			Incubation_Equilibration_Step = Latest_Incubate_Step
			Sample_Volume = Step.GetParameters()[VOLUME]
			Sample_Source = Step.GetParameters()[SOURCE]
			Equilibration_Buffer = Step.GetParameters()[EQUILIBRATION_BUFFER]
			Destination = Step.GetParentPlate()
			#I set these ahead of time because ths cannot change after equilibration. Best to lock it at the beginning

			SOLUTIONS.AddSolution(Equilibration_Buffer, SOLUTIONS.TYPE_BUFFER, SOLUTIONS.STORAGE_AMBIENT)
			SOLUTIONS.GetSolution(Equilibration_Buffer).AddVolume(Sample_Volume * SAMPLES.GetTotalSamples())

			PLATES.AddPlate("Desalting Waste", "96 Well PCR Plate", SAMPLES.GetSequences())
			PLATES.GetPlate("Desalting Waste").CreatePipetteSequence(SAMPLES.Column(""),SAMPLES.Column(1))
			#Volume of 1 added so the Waste solution is not deleted from the solutions list.
			#HCP analysis detected cross contamination, At this point it is better to use a plate for waste. In that way each sample is isolated to a well.

			PreferredLoading = CONFIGURATION.GetStepLoading(TITLE)
			CONFIGURATION.AddPreferredLoading("Desalting Waste", PreferredLoading["Waste"])
			CONFIGURATION.AddPreferredLoading(Equilibration_Buffer, PreferredLoading["Buffer"])
			CONFIGURATION.AddPreferredLoading(Destination, PreferredLoading["Destination"])


def Equilibrate():
	global Equilibrated
	global Sample_Volume
	global Equilibration_Buffer

	if Equilibrated == False:
		Equilibrated = True
		DESALT.Equilibrate(Equilibration_Buffer, Sample_Volume)

def Process():
	global Sample_Volume
	global Sample_Source
	global Equilibration_Buffer
	global Equilibrated
	global Destination

	PLATES.GetPlate(Destination).CreatePipetteSequence(SAMPLES.Column(Equilibration_Buffer), SAMPLES.Column(Sample_Volume))
	Equilibrated = False
	DESALT.Process(Destination, Equilibration_Buffer, Sample_Volume, Sample_Source)
		
def Step(step):
	Equilibrate()
	Process()