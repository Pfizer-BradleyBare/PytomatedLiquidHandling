from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...User import Samples as SAMPLES
from ...Hamilton.Commands import Pipette as PIPETTE
from ...User import Configuration as CONFIGURATION
from ...General import HamiltonIO as HAMILTONIO
import copy

TITLE = "Liquid Transfer"
NAME = "Name"
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
	DestinationPlate = step.GetParentPlate()
	
	SourceList = SAMPLES.Column(step.GetParameters()[NAME])
	SourceVolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])
	MixList = SAMPLES.Column(step.GetParameters()[MIXING])
	
	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, step.GetParameters()[TYPE], step.GetParameters()[STORAGE])

	Sequences = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(SourceList, SourceVolumeList,MixList)
	
	_Temp = copy.deepcopy(Sequences)
	for Sequence in _Temp:
			SOLUTIONS.GetSolution(Sequence["Source"]).AddVolume(Sequence["Volume"])
			SOLUTIONS.AddPipetteVolume(Sequence["Volume"])
	
	if HAMILTONIO.IsSimulated() == False:
		for sequence in Sequences:
			print(sequence["Destination"])
			sequence["Source"] = CONFIGURATION.GetDeckLoading(sequence["Source"])["Sequence"]
			sequence["Destination"] = CONFIGURATION.GetDeckLoading(sequence["Destination"])["Sequence"]
		DestinationPlate = CONFIGURATION.GetDeckLoading(DestinationPlate)["Sequence"]
	#Translate User defined names into sequence loading names

	if len(Sequences) != 0:
		PIPETTE.Do(DestinationPlate, Sequences)

