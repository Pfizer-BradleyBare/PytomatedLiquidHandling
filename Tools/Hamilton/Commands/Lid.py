from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Lid"
	return CommandString

def AcquireReservation(Input):
	CommandString = ""
	CommandString += "[Module]Lid"
	CommandString += "[Command]AcquireReservation"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString

def ReleaseReservation(Input):
	CommandString = ""
	CommandString += "[Module]Lid"
	CommandString += "[Command]ReleaseReservation"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString

def GetReservationLidSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]GetReservationLidSequenceString"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString

def GetReservationLidTansportType(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]GetReservationLidTansportType"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString

