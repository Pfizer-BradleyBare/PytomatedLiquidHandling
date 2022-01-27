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
TYPE = "Liquid Type"
STORAGE = "Storage Condition"
VOLUME = "Volume (uL)"
MIXING = "Mix?"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init():
	pass

def Step(step):

	LOG.BeginCommentsLog()
	
	DestinationPlate = step.GetParentPlate()

	SourceList = SAMPLES.Column(step.GetParameters()[NAME])
	SourceVolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])
	MixList = SAMPLES.Column(step.GetParameters()[MIXING])

	STATUS_UPDATE.AppendText("Transfering " +  str(step.GetParameters()[VOLUME]) + " uL of " + str(step.GetParameters()[TYPE]) + " to " + str(step.GetParentPlate()) + " plate ")
	
	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, step.GetParameters()[TYPE], step.GetParameters()[STORAGE])
	
	Sequence = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(SourceList, SourceVolumeList,MixList)
	
	for Counter in range(0,Sequence.GetNumSequencePositions()):
			SOLUTIONS.GetSolution(Sequence.GetSources()[Counter]).AddVolume(Sequence.GetTransferVolumes()[Counter])
			SOLUTIONS.AddPipetteVolume(Sequence.GetTransferVolumes()[Counter])

	if Sequence.GetNumSequencePositions() == 0:
		LOG.Comment("Number of sequences is zero so no liquid transfer will actually occur.")

	LOG.EndCommentsLog()

	if Sequence.GetNumSequencePositions() != 0:

		TransferVolumes = Sequence.GetTransferVolumes()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":len(TransferVolumes)*["Water"]}))
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}))

		Response = HAMILTONIO.SendCommands()

		if Response == False:
			LiquidClassStrings = []
			TipSequenceStrings = []
		else:
			LiquidClassStrings = Response[0]["Response"].split(HAMILTONIO.GetDelimiter())
			TipSequenceStrings = Response[1]["Response"].split(HAMILTONIO.GetDelimiter())

		HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":Sequence,"LiquidClasses":LiquidClassStrings,"TipSequences":TipSequenceStrings,"KeepTips":"False","DestinationPipettingOffset":0}))
		Response = HAMILTONIO.SendCommands()




