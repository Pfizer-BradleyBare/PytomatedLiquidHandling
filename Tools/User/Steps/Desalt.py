from ..Steps import Steps as STEPS
from ..Steps import Incubate as INCUBATE
from ..Labware import Solutions as SOLUTIONS
from ..Labware import Plates as PLATES
from ...User import Samples as SAMPLES
from ...User import Configuration as CONFIGURATION
from ...Hamilton.Commands import Desalt as DESALT
from ...General import Log as LOG
from ...Hamilton.Commands import StatusUpdate as STATUS_UPDATE
from ...General import HamiltonIO as HAMILTONIO

#This is per sample
DesaltingEQVolume = 900
DesaltingElutionVolume = 100
DesaltingRequiredTips = 3

#Step Args
TITLE = "IMCS SizeX Desalt"
SOURCE = "Source Plate"
WASTE = "Waste Plate"
EQUILIBRATION_BUFFER = "Equilibration Buffer"
TYPE = "Load Volume"
ELUTION_METHOD = "Elution Method"

#This variable tracks whether or not the tips have been equilibrated
Desalting_Params = {}
IsUsedFlag = False

######################################################################### 
#	Description: Returns the incubation step in which desalting equilibration is most logical
#	Input Arguments: N/A
#	Returns: [Step module Class]
#########################################################################
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
	global IsUsedFlag
	global Desalting_Params

	Desalting_Params = {}

	for Step in MutableStepsList:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			Parent = Step.GetParentPlateName()
			Params = Step.GetParameters()

			#Now we need to find the incubation step that comes before it
			SearchStep = Step
			while SearchStep.GetTitle() != INCUBATE.TITLE:
				SearchStep = STEPS.GetPreviousStepInPathway(SearchStep)

				if SearchStep == None:
					break

			Desalting_Params[Parent + str(Step.GetCoordinates())] = {\
				"Destination":Parent, \
				"Source":Params[SOURCE], \
				"Waste":Params[WASTE], \
				"EQ Buffer":Params[EQUILIBRATION_BUFFER], \
				"Volume":str(Params[TYPE]).replace(" ","").replace('.0','').split("+"), \
				"Method":Params[ELUTION_METHOD], \
				"EQ":False, \
				"EQ Step": SearchStep}

######################################################################### 
#	Description: Performs equilibration by calling the appropriate hamilton commands
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Equilibrate(ParentPlate):
	global Desalting_Params

	Params = Desalting_Params[ParentPlate]

	if Params["EQ"] == False:
		LOG.Comment("Performing Desalting Equilibration")
		Params["EQ"] = True
		LOG.BeginCommandLog()
		HAMILTONIO.AddCommand(DESALT.Equilibrate({"ParentPlate":ParentPlate, "StartPosition":SAMPLES.StartPosition}))
		Response = HAMILTONIO.SendCommands()
		LOG.EndCommandLog()
	else:
		LOG.Comment("Equilibration already performed. Skipping Equilibration")
		
	STATUS_UPDATE.AppendText("Performing Desalting Equilibration and Desalting Samples")	

######################################################################### 
#	Description: Performs equilibration and simulates a pipetting step into the destination plate
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Process(ParentPlate):
	global Desalting_Params

	Params = Desalting_Params[ParentPlate]

	#STATUS_UPDATE.AppendText("Performing Desalting Equilibration and Desalting Samples")
	Params["EQ"] = False
	LOG.BeginCommandLog()
	HAMILTONIO.AddCommand(DESALT.Process({"ParentPlate":ParentPlate, "StartPosition":SAMPLES.StartPosition}))
	Response = HAMILTONIO.SendCommands()
	LOG.EndCommandLog()
	
######################################################################### 
#	Description: Runs equilibration and processing
#	Input Arguments: [step: Step Class]
#	Returns: N/A
#########################################################################	
def Step(step):
	global Desalting_Params

	Params = step.GetParameters()
	Source = Params[SOURCE]
	Volume = sum(map(float,str(Params[TYPE]).replace(" ","").split("+"))) / 100
	Buffer = Params[EQUILIBRATION_BUFFER]
	EQ_Destination = Params[WASTE]
	Sample_Destination = step.GetParentPlateName()

	StepKey = step.GetParentPlateName() + str(step.GetCoordinates())

	EQ_Labware = PLATES.LABWARE.GetLabware(EQ_Destination)
	EQ_Labware.SetIsIMCSSizeXDesalting()

	EQ_DestinationNames = SAMPLES.Column(EQ_Destination)
	EQ_DestinationContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,EQ_DestinationNames)
	BufferNames = SAMPLES.Column(Buffer)
	BufferContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,BufferNames)
	SourceVolumes = SAMPLES.Column((DesaltingEQVolume + DesaltingElutionVolume) * Volume)
	MixingParameters = SAMPLES.Column("N/A")

	Sequence = PLATES.CreatePipetteSequence(EQ_DestinationContextualStrings,EQ_DestinationNames,BufferContextualStrings,BufferNames,SourceVolumes,MixingParameters, False)

	BufferLabware = PLATES.LABWARE.GetLabware(Buffer)
	BufferLabware.SetIsIMCSSizeXDesalting()

	Desalting_Params[StepKey]["Positions"] = Sequence.GetDestinationPositions()

	Equilibrate(StepKey)

	DestinationLabware = PLATES.LABWARE.GetLabware(Sample_Destination)
	DestinationLabware.SetIsIMCSSizeXDesalting()

	DestinationNames = SAMPLES.Column(Sample_Destination)
	DestinationContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,DestinationNames)
	SourceNames = SAMPLES.Column(Source)
	SourceContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,SourceNames)
	SourceVolumes = SAMPLES.Column(DesaltingElutionVolume * Volume)
	MixingParameters = SAMPLES.Column("N/A")

	Sequence = PLATES.CreatePipetteSequence(DestinationContextualStrings,DestinationNames,SourceContextualStrings,SourceNames,SourceVolumes,MixingParameters, False)
	Process(StepKey)

	
