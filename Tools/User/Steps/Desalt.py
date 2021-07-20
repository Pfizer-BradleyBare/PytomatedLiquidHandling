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
VOLUME = "Type"

#This variable tracks whether or not the tips have been equilibrated
Equilibrated = None
Required_Tips = 0
Sample_Volume = 0
Sample_Source = None
Equilibration_Buffer = None
Destination = None
Incubation_Equilibration_Step = None

######################################################################### 
#	Description: Returns the incubation step in which desalting equilibration is most logical
#	Input Arguments: N/A
#	Returns: [Step module Class]
#########################################################################
def GetEquilibrationStep():
	global Incubation_Equilibration_Step
	return Incubation_Equilibration_Step

######################################################################### 
#	Description: Initializes the desalting library by performing the following steps:
#	1. Iterate through all steps in MutableStepsList
#	2. If an incubation step is found, save that step
#	3. If a desalting step is found, set the latest incubation step as the most logical equilibration step.
#		Pull all step information. Add the equilibration buffer to the solutions list w/ used volume, and add a waste trough to the list of plates.
#		Finally, step the preferred loading positions for this step.
#	Input Arguments: [MutableStepsList: List]
#	Returns: N/A
#########################################################################
def Init(MutableStepsList):
	global Equilibrated
	global Incubation_Equilibration_Step
	global Sample_Volume
	global Sample_Source
	global Equilibration_Buffer
	global Destination
	global Required_Tips
	
	Equilibrated = False
	Latest_Incubate_Step = None



	for Step in MutableStepsList:
		if Step.GetTitle() == INCUBATE.TITLE:
			Latest_Incubate_Step = Step

		if Step.GetTitle() == TITLE:
			StepConfig = CONFIGURATION.GetStepConfig(TITLE)

			DesaltingArray = Step.GetParameters()[VOLUME].split(",")
			TypeArray = []
			VolumeArray = []
			for DesaltingStep in DesaltingArray:
				StepParams = DesaltingStep.split(":")
				TypeArray.append(StepParams[0].replace(" ",""))
				VolumeArray.append(float(StepParams[1].replace(" ","")))
			NumTipSets = len(DesaltingArray)

			Required_Tips = 3 * SAMPLES.GetTotalSamples()
			Incubation_Equilibration_Step = Latest_Incubate_Step
			Sample_Volume = sum(VolumeArray)
			Sample_Source = Step.GetParameters()[SOURCE]
			Equilibration_Buffer = Step.GetParameters()[EQUILIBRATION_BUFFER]
			Destination = Step.GetParentPlate()
			#I set these ahead of time because ths cannot change after equilibration. Best to lock it at the beginning

			SOLUTIONS.AddSolution(Equilibration_Buffer, SOLUTIONS.TYPE_BUFFER, SOLUTIONS.STORAGE_AMBIENT)
			for i in range(0,NumTipSets):
				SOLUTIONS.GetSolution(Equilibration_Buffer).AddVolume(StepConfig["Type"][TypeArray[i]][VolumeArray[i]]["Total Buffer Volume"] * SAMPLES.GetTotalSamples())

			PLATES.AddPlate("Desalting Waste", "96 Well PCR Plate", SAMPLES.GetSequences())
			PLATES.GetPlate("Desalting Waste").CreatePipetteSequence(SAMPLES.Column(""),SAMPLES.Column(1))
			#Volume of 1 added so the Waste solution is not deleted from the solutions list.
			#HCP analysis detected cross contamination, At this point it is better to use a plate for waste. In that way each sample is isolated to a well.

			PreferredLoading = StepConfig["Preferred Loading"]
			CONFIGURATION.AddPreferredLoading("Desalting Waste", PreferredLoading["Waste"])
			CONFIGURATION.AddPreferredLoading(Equilibration_Buffer, PreferredLoading["Buffer"])
			CONFIGURATION.AddPreferredLoading(Destination, PreferredLoading["Destination"])

######################################################################### 
#	Description: Performs equilibration by calling the appropriate hamilton commands
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Equilibrate():
	global Equilibrated
	global Sample_Volume
	global Equilibration_Buffer

	if Equilibrated == False:
		Equilibrated = True
		DESALT.Equilibrate(Equilibration_Buffer, Sample_Volume)

######################################################################### 
#	Description: Performs equilibration and simulates a pipetting step into the destination plate
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Process():
	global Sample_Volume
	global Sample_Source
	global Equilibration_Buffer
	global Equilibrated
	global Destination

	PLATES.GetPlate(Destination).CreatePipetteSequence(SAMPLES.Column(Equilibration_Buffer), SAMPLES.Column(Sample_Volume))
	Equilibrated = False
	DESALT.Process(Destination, Equilibration_Buffer, Sample_Volume, Sample_Source)
	
######################################################################### 
#	Description: Runs equilibration and processing
#	Input Arguments: [step: Step Class]
#	Returns: N/A
#########################################################################	
def Step(step):
	Equilibrate()
	Process()