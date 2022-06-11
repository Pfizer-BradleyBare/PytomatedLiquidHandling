from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...Hamilton.Commands import MagneticBeads as MAGNETICBEADS
from ...Hamilton.Commands import Transport as TRANSPORT
from ...Hamilton.Commands import StatusUpdate as STATUS_UPDATE
from ...Hamilton.Commands import Labware as LABWARE
from ...Hamilton.Commands import Pipette as PIPETTE
from ...Hamilton.Commands import Lid as LID
from ...User import Samples as SAMPLES
from ..Steps import Wait as WAIT
from ..Steps import Split_Plate as SPLIT_PLATE
from ...User import Configuration as CONFIGURATION
from ...General import Log as LOG
from ...General import HamiltonIO as HAMILTONIO

import time

TITLE = "Magnetic Beads"
MAGNETIC_BEADS_PLATE = "Magnetic Beads Plate"
STORAGE_BUFFER = "Storage Buffer"
BUFFER_VOLUME = "Storage Buffer Volume (uL)"
WAIT_TIME = "Hold Time (min)"
REPS = "Repetitions"

ParentPlateNames = set()


IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def DoesStatusUpdates():
	return True

######################################################################### 
#	Description: intialized through the following actions:
#	1. Load step specific configuration information and stores to be used later
#	2. Combines the HHS prefix with the plate sequence information and stores in a dictionary for later use. Additionally add all HHS and Lid sequences to the hamilton check sequences
#	Input Arguments: 
#	Returns: 
#########################################################################
def Init(MutableStepsList):
	global IsUsedFlag
	global ParentPlateNames

	for step in MutableStepsList:
		if step.GetTitle() == TITLE:
			IsUsedFlag = True
			ParentPlateNames.add(step.GetParameters()[MAGNETIC_BEADS_PLATE])

def GetUsedParentPlateNames():
	global ParentPlateNames
	return ParentPlateNames

RepsCompleted = 1

NumtoWordDict = { \
	"1":"first",\
	"2":"second",\
	"3":"third",\
	"4":"forth",\
	"5":"fifth",\
	"6":"sixth",\
	"7":"seventh",\
	"8":"eighth",\
	"9":"ninth",\
	"10":"tenth",\
	"11":"eleventh",\
	"12":"twelveth",}

def Callback(step):
	global RepsCompleted

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Starting " + NumtoWordDict[str(RepsCompleted)] + " followup of Magnetic Beads Block. Block Coordinates: " + str(step.GetCoordinates())}))
	HAMILTONIO.SendCommands()

	ParentPlate = step.GetParentPlateName()
	Params = step.GetParameters()
	BeadsPlate = Params[MAGNETIC_BEADS_PLATE]
	Buffer = Params[STORAGE_BUFFER]
	Volume = Params[BUFFER_VOLUME]
	Time = Params[WAIT_TIME]
	Reps = int(Params[REPS])

	DestinationNamesList = SAMPLES.Column(ParentPlate)
	DestinationContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,DestinationNamesList)
	SourceNamesList = SAMPLES.Column(BeadsPlate)
	SourceContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,SourceNamesList)
	SourceLabware = PLATES.LABWARE.GetLabware(BeadsPlate)
	SourceVolumesList = SourceLabware.VolumesList

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[BeadsPlate]}),False)
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[BeadsPlate]}),False)
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetMagneticRackPlateSequenceString({"PlateName":BeadsPlate}),False)
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetMagneticRackPlateTransportType({"PlateName":BeadsPlate}),False)
	#Get transport related info

	RemoveSequences = PLATES.CreatePipetteSequence(DestinationContextStringsList,DestinationNamesList,SourceContextStringsList,SourceNamesList,SourceVolumesList,SAMPLES.Column(0),SAMPLES.Column(0))
	TransferVolumes = RemoveSequences.GetTransferVolumes()
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetCondensedBeadsLiquidClassStrings({"PlateName":BeadsPlate, "TransferVolumes":TransferVolumes}),False)
	HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}),False)
	#For removing liquid from the plate

	DestinationNamesList = SAMPLES.Column(BeadsPlate)
	DestinationContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,DestinationNamesList)
	SourceNamesList = SAMPLES.Column(Buffer)
	SourceContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,SourceNamesList)
	SourceVolumesList = SAMPLES.Column(Volume)

	AddSequences = PLATES.CreatePipetteSequence(DestinationContextStringsList,DestinationNamesList,SourceContextStringsList,SourceNamesList,SourceVolumesList,SAMPLES.Column(0),SAMPLES.Column(50))
	TransferVolumes = AddSequences.GetTransferVolumes()
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetGeneralLiquidTransferLiquidClassStrings({"PlateName":BeadsPlate, "TransferVolumes":TransferVolumes}),False)
	HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}),False)
	#For adding buffer to the plate

	Response = HAMILTONIO.SendCommands()
	#Get information for moving the plate to the rack
	
	if Response == False:
		PlateSequence = ""
		PlateType = ""
		RackSequence = ""
		RackType = ""
		BeadsLiquidClass = []
		BeadsTipSeqs = []
		GeneralLiquidClass = []
		GeneralTipSeqs = []
	else:
		PlateSequence = Response.pop(0)["Response"]
		PlateType = Response.pop(0)["Response"]
		RackSequence = Response.pop(0)["Response"]
		RackType = Response.pop(0)["Response"]
		BeadsLiquidClass = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
		BeadsTipSeqs = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
		GeneralLiquidClass = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
		GeneralTipSeqs = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
	#Lets get the info we need to move the plate

	for Counter in range(0,RemoveSequences.GetNumSequencePositions()):
		RemoveSequences.GetSources()[Counter] = RackSequence
		RemoveSequences.GetDispenseCycles()[Counter] = 0
		RemoveSequences.GetAspirateCycles()[Counter] = 0
	#We need to modify the destination to be the magnetic beads plate sequence above. The liquid needs to move through the magnetic beads plate.
	#We also want to disable all mixing. ALWAYS. We do not want to disturb the beads before we pick them up

	if RemoveSequences.GetNumSequencePositions() != 0:
		TransferArgumentsDict = {\
			"SequenceClass":RemoveSequences,\
			"SourceLiquidClasses":BeadsLiquidClass,\
			"DestinationLiquidClasses":BeadsLiquidClass,\
			"TipSequences":BeadsTipSeqs,\
			"KeepTips":"False",\
			"DestinationPipettingOffset":0}

		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Removing all liquid from beads plate"}))
		HAMILTONIO.AddCommand(PIPETTE.Transfer(TransferArgumentsDict))
		Response = HAMILTONIO.SendCommands()
	#Remove the liquid

	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":RackType,"SourceSequenceString":RackSequence,"DestinationLabwareType":PlateType,"DestinationSequenceString":PlateSequence,"Park":"True","CheckExists":"After"}))
	Response = HAMILTONIO.SendCommands()
	#Remove the plate from the rack

	if AddSequences.GetNumSequencePositions() != 0:
		TransferArgumentsDict = {\
			"SequenceClass":AddSequences,\
			"SourceLiquidClasses":GeneralLiquidClass,\
			"DestinationLiquidClasses":GeneralLiquidClass,\
			"TipSequences":GeneralTipSeqs,\
			"KeepTips":"False",\
			"DestinationPipettingOffset":0}

		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Adding storage buffer to beads plate and mixing vigorously to resuspend beads"}))
		HAMILTONIO.AddCommand(PIPETTE.Transfer(TransferArgumentsDict))
		Response = HAMILTONIO.SendCommands()
	#Add the storage liquid

    #This finished a rep. We also assume that the rep starts in Step function.
	print("RepsCompleted",RepsCompleted)
	if RepsCompleted < Reps:

		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Moving beads plate to magnetic rack"}))
		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":PlateType,"SourceSequenceString":PlateSequence,"DestinationLabwareType":RackType,"DestinationSequenceString":RackSequence,"Park":"True","CheckExists":"After"}))
		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Adding block to timer list to condense beads for " + str(Time) + " minutes"}))
		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending " + NumtoWordDict[str(RepsCompleted)] + " followup of Magnetic Beads Block. Block Coordinates: " + str(step.GetCoordinates())}))
		Response = HAMILTONIO.SendCommands()
		#Move plate to rack
		
		RepsCompleted += 1
		WAIT.StartTimer(step, Time, Callback, "magnetic beads condense time")
		#Wait for beads to condense
	else:
		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending " + NumtoWordDict[str(RepsCompleted)] + " followup of Magnetic Beads Block. Block Coordinates: " + str(step.GetCoordinates())}))
		HAMILTONIO.SendCommands()

def Step(step):
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Starting Magnetic Beads Block. Block Coordinates: " + str(step.GetCoordinates())}))
	HAMILTONIO.SendCommands()
	
	global RepsCompleted
	RepsCompleted = 1

	ParentPlate = step.GetParentPlateName()
	Params = step.GetParameters()
	BeadsPlate = Params[MAGNETIC_BEADS_PLATE]
	BufferList = SAMPLES.Column(Params[STORAGE_BUFFER])
	VolumeList = SAMPLES.Column(Params[BUFFER_VOLUME])
	Time = Params[WAIT_TIME]
	Reps = Params[REPS]

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []
	
	#Is source the destination?
	if ParentPlate == BeadsPlate:
		MethodComments.append("The Magnetic Beads Plate parameter and parent plate (Destination) are the same. This doesn't make sense. Please correct.")

	#Testing Magnetic Beads Plate
	if not (type(BeadsPlate) is str):
		MethodComments.append("The Magnetic Beads Plate parameter you provided is a number. This parameter must contain letters. Please Correct.")
	else:
		TestLabware = PLATES.LABWARE.GetLabware(BeadsPlate)
		if TestLabware == None:
			MethodComments.append("The Magnetic Beads Plate parameter you provided is a solution. Only a plate name is acceptable. Please correct.")
		else:
			if TestLabware.GetLabwareType() == PLATES.LABWARE.LabwareTypes.Reagent:
				MethodComments.append("The Magnetic Beads Plate parameter you provided is a solution. Only a plate name is acceptable. Please correct.")

	#Testing Storage Buffer
	if not all(type(Buffer) is str for Buffer in BufferList):
		MethodComments.append("The Storage Buffer parameter you provided is a number. This parameter must contain letters. Please Correct")

	#Testing Storage Buffer Volume
	if not all(not (type(Volume) is str) for Volume in VolumeList):
		MethodComments.append("The Storage Buffer Volume parameter you provided is not a number. This parameter must be a number. Please Correct")

	if type(Time) is str:
		MethodComments.append("The Time parameter you provided is not a number. This parameter must be a number. Please Correct")

	if type(Reps) is str:
		MethodComments.append("The Repetitions parameter you provided is not a number. This parameter must be a number. Please Correct")

	if Reps > 12:
		MethodComments.append("The Repetitions parameter can be a max of 10. Please Correct")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################


	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[BeadsPlate]}),False)
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[BeadsPlate]}),False)
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetMagneticRackPlateSequenceString({"PlateName":BeadsPlate}),False)
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetMagneticRackPlateTransportType({"PlateName":BeadsPlate}),False)

	Response = HAMILTONIO.SendCommands()
	#Get information for moving the plate to the rack

	if Response == False:
		PlateSequence = ""
		PlateType = ""
		RackSequence = ""
		RackType = ""
	else:
		PlateSequence = Response.pop(0)["Response"]
		PlateType = Response.pop(0)["Response"]
		RackSequence = Response.pop(0)["Response"]
		RackType = Response.pop(0)["Response"]
	#Lets get the info we need to move the plate

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Moving beads plate to magnetic rack"}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":PlateType,"SourceSequenceString":PlateSequence,"DestinationLabwareType":RackType,"DestinationSequenceString":RackSequence,"Park":"True","CheckExists":"After"}))
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Adding block to timer list to condense beads for " + str(Time) + " minutes"}))
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending Magnetic Beads Block. Block Coordinates: " + str(step.GetCoordinates())}))
	Response = HAMILTONIO.SendCommands()
	#Move plate to rack
		
	WAIT.StartTimer(step, Time, Callback, "magnetic beads condense time")
	#Wait for beads to condense
		




