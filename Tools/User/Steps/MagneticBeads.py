from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
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
REPS = "Repititions"

ParentPlateNames = set()


IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag


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
			ParentPlateNames.add(step.GetParentPlate())

def GetUsedParentPlateNames():
	global ParentPlateNames
	return ParentPlateNames

RepsCompleted = 1

def Callback(step):
	global RepsCompleted

	ParentPlate = step.GetParentPlate()
	Params = step.GetParameters()
	BeadsPlate = Params[MAGNETIC_BEADS_PLATE]
	Buffer = Params[STORAGE_BUFFER]
	Volume = Params[BUFFER_VOLUME]
	Time = Params[WAIT_TIME]
	Reps = int(Params[REPS])

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[ParentPlate]}))
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[ParentPlate]}))
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetMagneticRackPlateSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetMagneticRackPlateTransportType({"PlateName":ParentPlate}))
	#Get transport related info

	RemoveSequences = PLATES.GetPlate(ParentPlate).CreatePipetteSequence(SAMPLES.Column(BeadsPlate), PLATES.GetPlate(BeadsPlate).GetVolumes(), SAMPLES.Column("No"))
	TransferVolumes = RemoveSequences.GetTransferVolumes()
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetCondensedBeadsLiquidClassStrings({"PlateName":ParentPlate, "TransferVolumes":TransferVolumes}))
	HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}))
	#For removing liquid from the plate

	AddSequences = PLATES.GetPlate(BeadsPlate).CreatePipetteSequence(SAMPLES.Column(Buffer), SAMPLES.Column(Volume), SAMPLES.Column("After"))
	TransferVolumes = AddSequences.GetTransferVolumes()
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetGeneralLiquidTransferLiquidClassStrings({"PlateName":ParentPlate, "TransferVolumes":TransferVolumes}))
	HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}))
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
		BeadsLiquidClass = Response.pop(0)["Response"]
		BeadsTipSeqs = Response.pop(0)["Response"]
		GeneralLiquidClass = Response.pop(0)["Response"]
		GeneralTipSeqs = Response.pop(0)["Response"]
	#Lets get the info we need to move the plate

	HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":RemoveSequences,"LiquidClasses":BeadsLiquidClass,"TipSequences":BeadsTipSeqs,"KeepTips":"False","DestinationPipettingOffset":0}))
	#Remove the liquid

	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":RackType,"SourceSequenceString":RackSequence,"DestinationLabwareType":PlateType,"DestinationSequenceString":PlateSequence,"Park":"True","CheckExists":"After"}))
	#Remove the plate from the rack
		
	HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":AddSequences,"LiquidClasses":GeneralLiquidClass,"TipSequences":GeneralTipSeqs,"KeepTips":"False","DestinationPipettingOffset":0}))
	Response = HAMILTONIO.SendCommands()
	#Add the storage liquid

	#This finished a rep. We also assume that the rep starts in Step function.
	print("RepsCompleted",RepsCompleted)
	if RepsCompleted < Reps:
		RepsCompleted += 1

		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":PlateType,"SourceSequenceString":PlateSequence,"DestinationLabwareType":RackType,"DestinationSequenceString":RackSequence,"Park":"True","CheckExists":"After"}))
		Response = HAMILTONIO.SendCommands()
		#Move plate to rack
		
		WAIT.StartTimer(step, Time, Callback)
		#Wait for beads to condense

def Step(step):
	global RepsCompleted
	RepsCompleted = 1

	LOG.BeginCommentsLog()
	LOG.EndCommentsLog()

	ParentPlate = step.GetParentPlate()
	Params = step.GetParameters()
	BeadsPlate = Params[MAGNETIC_BEADS_PLATE]
	Buffer = Params[STORAGE_BUFFER]
	Volume = Params[BUFFER_VOLUME]
	Time = Params[WAIT_TIME]

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[ParentPlate]}))
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[ParentPlate]}))
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetMagneticRackPlateSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(MAGNETICBEADS.GetMagneticRackPlateTransportType({"PlateName":ParentPlate}))

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

	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":PlateType,"SourceSequenceString":PlateSequence,"DestinationLabwareType":RackType,"DestinationSequenceString":RackSequence,"Park":"True","CheckExists":"After"}))
	Response = HAMILTONIO.SendCommands()
	#Move plate to rack
		
	WAIT.StartTimer(step, Time, Callback)
	#Wait for beads to condense
		




