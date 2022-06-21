from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...User import Samples as SAMPLES
from ...Hamilton.Commands import Pipette as PIPETTE
from ...Hamilton.Commands import Transport as TRANSPORT
from ...Hamilton.Commands import StatusUpdate as STATUS_UPDATE
from ...User import Configuration as CONFIGURATION
from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG
import copy

TITLE = "Liquid Transfer"
NAME = "Source"
VOLUME = "Volume (uL)"
MIXING = "Mix?"

IsUsedFlag = True

def IsUsed():
	return IsUsedFlag

def DoesStatusUpdates():
	return True

def Init():
	pass

def Step(step):
	
	DestinationPlateName = STEPS.Class.GetParentPlateName(step)

	Source = step.GetParameters()[NAME]
	Volume = step.GetParameters()[VOLUME]

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Starting Liquid Transfer Block. Block Coordinates: " + str(step.GetCoordinates())}),False,True)
	HAMILTONIO.SendCommands()

	DestinationNamesList = SAMPLES.Column(DestinationPlateName)
	DestinationContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,DestinationNamesList)
	SourceNamesList = SAMPLES.Column(Source)
	SourceContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,SourceNamesList)
	SourceVolumesList = SAMPLES.Column(Volume)
	MixingList = SAMPLES.Column(step.GetParameters()[MIXING])

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []
	
	#Is source the destination?
	if DestinationPlateName in SourceNamesList:
		MethodComments.append("The Source parameter and parent plate (Destination) are the same. This doesn't make sense. Please correct.")

	#Testing Source
	if not all(type(Source) is str for Source in SourceNamesList):
		MethodComments.append("The Source parameter you provided is a number. This parameter must contain letters. Please Correct")

	#Testing Volume
	if not all(not (type(Volume) is str) for Volume in SourceVolumesList):
		MethodComments.append("The Volume parameter you provided is not a number. This parameter must be a number. Please Correct")

	#Testing Mix
	if not all(type(Mix) is str for Mix in MixingList):
		MethodComments.append("The Mix parameter you provided is a number. This parameter must contain letters. Please Correct")
	elif not all(Mix == "No" or "Dispense:" in Mix or "Aspirate:" in Mix for Mix in MixingList):
		MethodComments.append("The Mix parameter you provided is incorrect. This parameter must come from the dropdown. Please Correct")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)
		if HAMILTONIO.IsSimulated() == True:
			quit()
		else:
			STEPS.UpdateStepParams(step)
			Step(step)
			return

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	AspList = []
	DisList = []
	for Mix in MixingList:
		MixDict = {"Aspirate":0, "Dispense": 0}

		if Mix != "No":
			Mix = Mix.replace(" ","")
			#Remove Spaces
			Mix = Mix.split("+")
			
			for MixItem in Mix:
				MixItem = MixItem.split(":")
				MixDict[MixItem[0]] = int(MixItem[1])

		AspList.append(MixDict["Aspirate"])
		DisList.append(MixDict["Dispense"])
	#Parse our mixing parameter

	Sequence = PLATES.CreatePipetteSequence(DestinationContextStringsList,DestinationNamesList,SourceContextStringsList,SourceNamesList,SourceVolumesList,AspList,DisList)

	if Sequence.GetNumSequencePositions() == 0:
		#LOG.Comment("Number of sequences is zero so no liquid transfer will actually occur.")
		pass

	if Sequence.GetNumSequencePositions() != 0:

		TransferVolumes = Sequence.GetTransferVolumes()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":Sequence.GetSourceLiquidClassStrings()}),False)
		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":Sequence.GetDestinationLiquidClassStrings()}),False)
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}),False)

		Response = HAMILTONIO.SendCommands()

		if Response == False:
			SourceLiquidClassStrings = []
			DestinationLiquidClassStrings = []
			TipSequenceStrings = []
		else:
			SourceLiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
			DestinationLiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
			TipSequenceStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())


		TransferArgumentsDict = {\
			"SequenceClass":Sequence,\
			"SourceLiquidClasses":SourceLiquidClassStrings,\
			"DestinationLiquidClasses":DestinationLiquidClassStrings,\
			"TipSequences":TipSequenceStrings,\
			"KeepTips":"False",\
			"DestinationPipettingOffset":0}

		if SAMPLES.InColumn(Source) == True:
			SourceString = str(Source) + " (WC)"
		else:
			SourceString = str(Source)

		if SAMPLES.InColumn(Volume) == True:
			VolumeString = str(Volume) + " (WC)"
		else:
			VolumeString = str(Volume) + " uL"

		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Transferring " + VolumeString + " of " + SourceString + " to " + DestinationPlateName}),False,True)
		HAMILTONIO.AddCommand(PIPETTE.Transfer(TransferArgumentsDict))
		Response = HAMILTONIO.SendCommands()

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending Liquid Transfer Block. Block Coordinates: " + str(step.GetCoordinates())}),False,True)
	HAMILTONIO.SendCommands()



