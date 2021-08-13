from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(HeaterList):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Heater]\n"
	for Heater in HeaterList:
		CommandString += "[ID]" + str(Heater["ID"]) + "[Type]" + str(Heater["Type"]) + "\n"
	
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

def StartHeating(ID, Temp):
	CommandString = ""
	CommandString += str(LOG.GetCommandID()) + "[Heater]\n"
	CommandString += "[Start Heat]\n"
	CommandString += "[ID]" + str(ID) + "[Temp]" + str(Temp) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
	return True

def StopHeating(ID):
	CommandString = ""
	CommandString += str(LOG.GetCommandID()) + "[Heater]\n"
	CommandString += "[Stop Heat]\n"
	CommandString += "[ID]" + str(ID) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
	return True

def StartShaking(ID, RPM):
	CommandString = ""
	CommandString += str(LOG.GetCommandID()) + "[Heater]\n"
	CommandString += "[Start Shake]\n"
	CommandString += "[ID]" + str(ID) + "[RPM]" + str(RPM) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
	return True

def StopShaking(ID):
	CommandString = ""
	CommandString += str(LOG.GetCommandID()) + "[Heater]\n"
	CommandString += "[Stop Shake]\n"
	CommandString += "[ID]" + str(ID) + "\n"
	
	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
	return True






