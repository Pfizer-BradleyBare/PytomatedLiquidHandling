from ..General import HamiltonIO as HAMILTONIO
from ..Hamilton.Commands import Desalt as DESALT
from ..Hamilton.Commands import Heater as HEATER
from ..Hamilton.Commands import Vacuum as VACUUM
from ..Hamilton.Commands import Notify as NOTIFY
from ..Hamilton.Commands import Pipette as PIPETTE
from ..Hamilton.Commands import Timer as TIMER
from ..Hamilton.Commands import Transport as TRANSPORT


def CheckSequences(SequencesList):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Check Sequences]\n"
	for Sequence in SequencesList:
		CommandString += "[Sequence]" + str(Sequence) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	

#This function send the loading list to the Hamilton.
def Labware(LoadingList):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Labware]\n"
	for Labware in LoadingList:
		CommandString += "[Name]" + str(Labware) + "[LabwareSequence]" + str(LoadingList[Labware]["Sequence"]) + "[LidSequence]" + str(LoadingList[Labware]["Lid"])  
		CommandString += "[LoadingLocation]" + str(LoadingList[Labware]["LoadingPosition"])
		if str(LoadingList[Labware]["Labware Category"]) == "Plates":
			CommandString += "[Volume]" + str(LoadingList[Labware]["Max Volume"])
		else:
			CommandString += "[Volume]" + str(LoadingList[Labware]["Volume"])
		CommandString += "[LabwareType]" + str(LoadingList[Labware]["Labware Type"]) + "[LabwareCategory]" + str(LoadingList[Labware]["Labware Category"]) + "\n"

	print(CommandString)

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

def Samples(NumSamples):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Samples]\n"
	CommandString += "[SampleNumber]" + str(NumSamples) + "\n"
	
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True


