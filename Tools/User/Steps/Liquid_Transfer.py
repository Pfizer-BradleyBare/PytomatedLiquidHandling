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

def Init():
	pass

def Step(step):
	LOG.BeginCommentsLog()
	
	DestinationPlateName = STEPS.Class.GetParentPlateName(step)

	DestinationNamesList = SAMPLES.Column(DestinationPlateName)
	DestinationContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,DestinationNamesList)
	SourceNamesList = SAMPLES.Column(step.GetParameters()[NAME])
	SourceContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,SourceNamesList)
	SourceVolumesList = SAMPLES.Column(step.GetParameters()[VOLUME])
	MixingList = SAMPLES.Column(step.GetParameters()[MIXING])

	Sequence = PLATES.CreatePipetteSequence(DestinationContextStringsList,DestinationNamesList,SourceContextStringsList,SourceNamesList,SourceVolumesList,MixingList)

	if Sequence.GetNumSequencePositions() == 0:
		LOG.Comment("Number of sequences is zero so no liquid transfer will actually occur.")

	LOG.EndCommentsLog()

	if Sequence.GetNumSequencePositions() != 0:

		TransferVolumes = Sequence.GetTransferVolumes()
		LiquidClassStrings = Sequence.GetLiquidClassStrings()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":LiquidClassStrings}))
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




