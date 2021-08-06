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
TYPE = "Type"

#This variable tracks whether or not the tips have been equilibrated
Equilibrated = None
Incubation_Equilibration_Step = None
Desalting_Params = {}
IsUsedFlag = False

######################################################################### 
#	Description: Returns the incubation step in which desalting equilibration is most logical
#	Input Arguments: N/A
#	Returns: [Step module Class]
#########################################################################
def GetEquilibrationStep():
	global Incubation_Equilibration_Step
	return Incubation_Equilibration_Step

def GetDesaltParams():
	global Desalting_Params
	return Desalting_Params

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

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
	global Desalting_Params
	global IsUsedFlag
	
	Equilibrated = False
	Latest_Incubate_Step = None

	for Step in MutableStepsList:
		if Step.GetTitle() == INCUBATE.TITLE:
			Latest_Incubate_Step = Step

		if Step.GetTitle() == TITLE:
			StepConfig = CONFIGURATION.GetStepConfig(TITLE)
			IsUsedFlag = True

			DesaltingArray = Step.GetParameters()[TYPE].split(",")
			TypeArray = []
			VolumeArray = []
			for DesaltingStep in DesaltingArray:
				StepParams = DesaltingStep.split(":")
				TypeArray.append(StepParams[0].replace(" ",""))
				VolumeArray.append(StepParams[1].replace(" ",""))
			NumTipSets = len(DesaltingArray)
			#Get Desalting details

			Incubation_Equilibration_Step = Latest_Incubate_Step
			#I set these ahead of time because ths cannot change after equilibration. Best to lock it at the beginning

			Desalting_Params["Required Tips"] = 3 * SAMPLES.GetTotalSamples()
			Desalting_Params["Type"] = ','.join(TypeArray)
			Desalting_Params["Volume"] = ','.join(VolumeArray)
			Desalting_Params["Source"] = Step.GetParameters()[SOURCE]
			Desalting_Params["Buffer"] = Step.GetParameters()[EQUILIBRATION_BUFFER]
			Desalting_Params["Destination"] = Step.GetParentPlate()

			Source = CONFIGURATION.GetDeckLoading(Step.GetParameters()[SOURCE])
			Buffer = CONFIGURATION.GetDeckLoading(Step.GetParameters()[EQUILIBRATION_BUFFER])
			Destination = CONFIGURATION.GetDeckLoading(Step.GetParentPlate())
			Waste = CONFIGURATION.GetDeckLoading("Desalting Waste")

			Desalting_Params["Source Sequence"] = Step.GetParameters()[SOURCE] if Source == None else Source["Sequence"]
			Desalting_Params["Buffer Sequence"] = Step.GetParameters()[EQUILIBRATION_BUFFER] if Buffer == None else Buffer["Sequence"]
			Desalting_Params["Waste Sequence"] = "Desalting Waste" if Waste == None else Waste["Sequence"]
			Desalting_Params["Destination Sequence"] = Step.GetParentPlate() if Destination == None else Destination["Sequence"]

			SOLUTIONS.AddSolution(Desalting_Params["Buffer"], SOLUTIONS.TYPE_BUFFER, SOLUTIONS.STORAGE_AMBIENT)
			for i in range(0,NumTipSets):
				SOLUTIONS.GetSolution(Desalting_Params["Buffer"]).AddVolume(StepConfig["Type"][TypeArray[i]][float(VolumeArray[i])]["Total Buffer Volume"] * SAMPLES.GetTotalSamples())

			PLATES.AddPlate("Desalting Waste", "96 Well PCR Plate", SAMPLES.GetSequences())
			PLATES.GetPlate("Desalting Waste").CreatePipetteSequence(SAMPLES.Column(""),SAMPLES.Column(1),SAMPLES.Column("Yes"))
			#Volume of 1 added so the Waste solution is not deleted from the solutions list.
			#HCP analysis detected cross contamination, At this point it is better to use a plate for waste. In that way each sample is isolated to a well.

			PreferredLoading = StepConfig["Preferred Loading"]
			CONFIGURATION.AddPreferredLoading("Desalting Waste", PreferredLoading["Waste"])
			CONFIGURATION.AddPreferredLoading(Desalting_Params["Buffer"], PreferredLoading["Buffer"])
			CONFIGURATION.AddPreferredLoading(Desalting_Params["Destination"], PreferredLoading["Destination"])

######################################################################### 
#	Description: Performs equilibration by calling the appropriate hamilton commands
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Equilibrate():
	global Equilibrated

	if Equilibrated == False:
		Equilibrated = True
		DESALT.Equilibrate()

######################################################################### 
#	Description: Performs equilibration and simulates a pipetting step into the destination plate
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Process():
	global Desalting_Params
	global Equilibrated

	Destination = Desalting_Params["Destination"]
	Buffer = Desalting_Params["Buffer"]
	Volume = sum(list(map(int, Desalting_Params["Volume"].split(","))))

	PLATES.GetPlate(Destination).CreatePipetteSequence(SAMPLES.Column(Buffer), SAMPLES.Column(Volume), SAMPLES.Column("Yes"))
	Equilibrated = False
	DESALT.Process()
	
######################################################################### 
#	Description: Runs equilibration and processing
#	Input Arguments: [step: Step Class]
#	Returns: N/A
#########################################################################	
def Step(step):
	Equilibrate()
	Process()