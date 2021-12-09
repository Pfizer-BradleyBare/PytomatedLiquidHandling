from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(HeaterList):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Heater"
	for Heater in HeaterList:
		CommandString += "[ID]" + str(Heater["ID"]) + "[Type]" + str(Heater["Type"]) + "\n"
	
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

def StartHeating(ID, Temp):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]Start Heat"
	CommandString += "[ID]" + str(ID) + "[Temp]" + str(Temp) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		#LOG.CommandID()
		#Do not log because we do not want heating disabled on a method resume
	return True

def StopHeating(ID):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]Stop Heat"
	CommandString += "[ID]" + str(ID) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		#LOG.CommandID()
		#Do not log because we do not want heating disabled on a method resume. Similar to above
	return True

def StartShaking(ID, RPM):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]Start Shake"
	CommandString += "[ID]" + str(ID) + "[RPM]" + str(RPM) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True

def StopShaking(ID):
	CommandString = ""
	CommandString += "[Module]Heater"
	CommandString += "[Command]Stop Shake"
	CommandString += "[ID]" + str(ID) + "\n"
	
	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True






