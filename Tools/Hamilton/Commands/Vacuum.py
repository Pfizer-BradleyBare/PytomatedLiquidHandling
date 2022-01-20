from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Vacuum"
	CommandString += "[ID]" + str(Input["ID"]) + "[Plate]" + str(Input["Plate"])
	return CommandString

#this function will start a timer for a specified plate
def Start(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]Start"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"]) + "[VacuumPressure]" + str(Input["VacuumPressure"])
	return CommandString
	
def Stop(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]Stop"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumCollectionPlateSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumCollectionPlateSequenceString"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumManifoldParkSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumManifoldParkSequenceString"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumManifoldSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumManifoldSequenceString"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumPlateSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumPlateSequenceString"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString