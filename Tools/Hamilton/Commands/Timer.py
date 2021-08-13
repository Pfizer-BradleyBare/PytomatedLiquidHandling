from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun():
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Timer]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will start a timer for a specified plate
def Start(WaitTime):
	CommandString = ""
	CommandString += str(LOG.GetCommandID()) + "[Timer]\n"
	CommandString += "[Start]\n"
	CommandString += "[Time]" + "{0:.2f}".format(WaitTime) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
	return True
	
#this function will wait on a plate timer
def Wait():
	CommandString = ""
	CommandString += str(LOG.GetCommandID()) + "[Timer]\n"
	CommandString += "[Wait]\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
	return True


