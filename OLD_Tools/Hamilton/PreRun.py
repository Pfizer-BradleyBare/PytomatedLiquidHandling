from ..General import HamiltonIO as HAMILTONIO
from ..Hamilton.Commands import Desalt as DESALT
from ..Hamilton.Commands import Heater as HEATER
from ..Hamilton.Commands import Vacuum as VACUUM
from ..Hamilton.Commands import Notify as NOTIFY
from ..Hamilton.Commands import Pipette as PIPETTE
from ..Hamilton.Commands import Timer as TIMER
from ..Hamilton.Commands import Transport as TRANSPORT
from ..Hamilton.Commands import Log as LOG
from ..Hamilton.Commands import Lid as LID
from ..Hamilton.Commands import StatusUpdate as STATUS_UPDATE
from ..Hamilton.Commands import MagneticBeads as MAGNETIC_BEADS


def CheckSequences(SequencesList):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Check Sequences"
	SequencesString = ""
	for Sequence in SequencesList:
		SequencesString += str(Sequence) + HAMILTONIO.GetDelimiter()
	CommandString += "[Sequence]" + SequencesString[:-1]
	return CommandString
	

#This function send the loading list to the Hamilton.
def Labware(LoadingList):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Labware"


	Names = ""
	LabwareSequences = ""
	LidSequences = ""
	LoadingLocations = ""
	LabwareVolumes = ""
	LabwareTypes = ""
	LabwareCategories = ""
	LabwareNames = ""

	for Labware in LoadingList:
		Names += str(Labware) + HAMILTONIO.GetDelimiter()
		LabwareSequences += str(LoadingList[Labware]["Sequence"]) + HAMILTONIO.GetDelimiter()
		LidSequences += str(LoadingList[Labware]["Lid"]) + HAMILTONIO.GetDelimiter()
		LoadingLocations += str(LoadingList[Labware]["LoadingPosition"]) + HAMILTONIO.GetDelimiter()

		if str(LoadingList[Labware]["Labware Info"]["Labware Category"]) == "Plates":
			LabwareVolumes += str(LoadingList[Labware]["Labware Info"]["Max Supported Volume"]) + HAMILTONIO.GetDelimiter()
		else:
			LabwareVolumes += str(LoadingList[Labware]["Used Volume"]) + HAMILTONIO.GetDelimiter()

		LabwareTypes += str(LoadingList[Labware]["Labware Info"]["Labware Type"]) + HAMILTONIO.GetDelimiter()
		LabwareCategories += str(LoadingList[Labware]["Labware Info"]["Labware Category"]) + HAMILTONIO.GetDelimiter()
		LabwareNames += str(LoadingList[Labware]["Labware Name"]) + HAMILTONIO.GetDelimiter()

	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Labware"
	CommandString += "[Name]" + Names[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[LabwareSequence]" + LabwareSequences[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[LidSequence]" + LidSequences[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[LoadingLocation]" + LoadingLocations[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[Volume]" + LabwareVolumes[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[LabwareType]" + LabwareTypes[:-1*len(HAMILTONIO.GetDelimiter())]  
	CommandString += "[LabwareCategory]" + LabwareCategories[:-1*len(HAMILTONIO.GetDelimiter())]  
	CommandString += "[LabwareName]" + LabwareNames[:-1*len(HAMILTONIO.GetDelimiter())] 
	return CommandString

def Samples(NumSamples):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Samples"
	CommandString += "[SampleNumber]" + str(NumSamples)
	return CommandString


