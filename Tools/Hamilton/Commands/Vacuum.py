from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Vacuum"
	CommandString += "[VacuumPlateNames]" + HAMILTONIO.GetDelimiter().join(Input["VacuumPlateNames"])
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

def GetVacuumCollectionPlateTransportType(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumCollectionPlateTransportType"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumParkSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumParkSequenceString"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumParkTransportType(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumParkTransportType"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumManifoldSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumManifoldSequenceString"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumManifoldTransportType(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumManifoldTransportType"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString

def GetVacuumPlateSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]GetVacuumPlateSequenceString"
	CommandString += "[VacuumPlateName]" + str(Input["VacuumPlateName"])
	return CommandString