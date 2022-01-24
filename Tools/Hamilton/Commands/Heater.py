from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Heater"
	return CommandString

def AcquireReservation(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]AcquireReservation"
	CommandString += "[PlateName]" + str(Input["PlateName"]) + "[Temperature]" + str(Input["Temperature"]) + "[RPM]" + str(Input["RPM"])
	return CommandString

def ConfirmReservation(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]ConfirmReservation"
	CommandString += "[PlateName]" + str(Input["PlateName"]) + "[Temperature]" + str(Input["Temperature"])
	return CommandString

def StartReservation(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]StartReservation"
	CommandString += "[PlateName]" + str(Input["PlateName"]) + "[Temperature]" + str(Input["Temperature"]) + "[RPM]" + str(Input["RPM"])
	return CommandString

def EndReservation(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]EndReservation"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString

def ReleaseReservation(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
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

def GetReservationHeaterSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]GetReservationHeaterSequenceString"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString

def GetReservationHeaterTansportType(Input):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]GetReservationHeaterTansportType"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString






def StartHeating(ID, Temp):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]Start Heat"
	CommandString += "[ID]" + str(ID) + "[Temp]" + str(Temp)
	return CommandString

def StopHeating(ID):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]Stop Heat"
	CommandString += "[ID]" + str(ID)
	return CommandString

def StartShaking(ID, RPM):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]Start Shake"
	CommandString += "[ID]" + str(ID) + "[RPM]" + str(RPM)
	return CommandString

def StopShaking(ID):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]Stop Shake"
	CommandString += "[ID]" + str(ID)
	return CommandString






