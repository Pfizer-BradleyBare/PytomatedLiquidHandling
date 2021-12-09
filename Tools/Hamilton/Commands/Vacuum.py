from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Params):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Vacuum"
	CommandString += "[ID]" + str(Params["ID"]) + "[Plate]" + str(Params["Plate"]) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will start a timer for a specified plate
def Start(Pressure, Time):
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]Start"
	CommandString += "[Pressure]" + str(Pressure) + "[Time]" + str(Time) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True
	
#this function will wait on a plate timer
def Wait():
	CommandString = ""
	CommandString += "[Module]Vacuum"
	CommandString += "[Command]Wait"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True


