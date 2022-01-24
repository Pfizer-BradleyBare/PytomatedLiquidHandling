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

def CreateStep(DestinationPlate, Source, Type, Storage, Volume, Mixing):
	NewStep = STEPS.Class(TITLE)
	NewStep.SetCoordinates(STEPS.NOT_EXCEL_COORDINATES[0],STEPS.NOT_EXCEL_COORDINATES[1])
	NewStep.SetParentPlateStep(DestinationPlate)

	NewStep.AddParameters(NAME, Source)
	NewStep.AddParameters(TYPE, Type)
	NewStep.AddParameters(STORAGE, Storage)
	NewStep.AddParameters(VOLUME, Volume)
	NewStep.AddParameters(MIXING, Mixing)

	return NewStep

def Step(step):

	LOG.BeginCommentsLog()

	
	DestinationPlate = step.GetParentPlate()

	SourceList = SAMPLES.Column(step.GetParameters()[NAME])
	SourceVolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])
	MixList = SAMPLES.Column(step.GetParameters()[MIXING])

	STATUS_UPDATE.AppendText("Transfering " +  str(step.GetParameters()[VOLUME]) + " uL of " + str(step.GetParameters()[TYPE]) + " to " + str(step.GetParentPlate()) + " plate ")
	
	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, step.GetParameters()[TYPE], step.GetParameters()[STORAGE])

	
	Sequences = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(SourceList, SourceVolumeList,MixList)
	
	_Temp = copy.deepcopy(Sequences)
	for Sequence in _Temp:
			SOLUTIONS.GetSolution(Sequence["Source"]).AddVolume(Sequence["Volume"])
			SOLUTIONS.AddPipetteVolume(Sequence["Volume"])

	if len(Sequences) == 0:
		LOG.Comment("Number of sequences is zero so no liquid transfer will actually occur.")

	LOG.EndCommentsLog()

	if len(Sequences) != 0:

		TransferVolumes = [str(x["Volume"]) for x in Sequences]

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings(TransferVolumes,["Water"]*len(TransferVolumes)))
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings(TransferVolumes))

		Response = HAMILTONIO.SendCommands()

		if Response == False:
			LiquidClassStrings = []
			TipSequenceStrings = []
		else:
			LiquidClassStrings = Response[0]["LiquidClassStrings"].split(HAMILTONIO.GetDelimiter())
			TipSequenceStrings = Response[1]["TipSequenceStrings"].split(HAMILTONIO.GetDelimiter())

		HAMILTONIO.AddCommand(PIPETTE.Transfer(Sequences,LiquidClassStrings,TipSequenceStrings))
		Response = HAMILTONIO.SendCommands()




