from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Params):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Vacuum]\n"
	CommandString += "[ID]" + str(Params["ID"]) + "[Plate]" + str(Params["Plate"]) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will start a timer for a specified plate
def Start(Pressure, Time):
	CommandString = ""
	CommandString += "[Vacuum]\n"
	CommandString += "[Start]\n"
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
	CommandString += "[Vaccum]\n"
	CommandString += "[Wait]\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True


