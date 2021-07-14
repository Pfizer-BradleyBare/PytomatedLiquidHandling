from ..General import HamiltonIO as HAMILTONIO

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
			CommandString += "[Volume]" + str(LoadingList[Labware]["MaxVolume"])
		else:
			CommandString += "[Volume]" + str(LoadingList[Labware]["Volume"])
		CommandString += "[LabwareType]" + str(LoadingList[Labware]["Labware Type"]) + "[LabwareCategory]" + str(LoadingList[Labware]["Labware Category"]) + "\n"

	print(CommandString)
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function send a list of pipetting steps to the Hamilton. From this list, the Hamilton will determine how many tips are used
def Tips(TipsList):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Tips]\n"
	for Tip in TipsList:
		CommandString += "[Tip]" + str(Tip) + "[Num]" + str(TipsList[Tip]["Used"]) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

