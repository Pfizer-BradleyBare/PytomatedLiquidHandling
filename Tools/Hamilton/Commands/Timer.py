from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun():
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Timer"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will start a timer for a specified plate
def Start(WaitTime):
	CommandString = ""
	CommandString += "[Module]Timer"
	CommandString += "[Command]Start"
	CommandString += "[Time]" + "{0:.2f}".format(WaitTime) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True
	
#this function will wait on a plate timer
def Wait():
	CommandString = ""
	CommandString += "[Module]Timer"
	CommandString += "[Command]Wait"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True


