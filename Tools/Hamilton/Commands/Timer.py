from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Timer"
	return CommandString

#this function will start a timer for a specified plate
def Start(Input):
	CommandString = ""
	CommandString += "[Module]Timer"
	CommandString += "[Command]Start"
	CommandString += "[WaitTime]" + "{0:.2f}".format(Input["WaitTime"])
	return CommandString
	
#this function will wait on a plate timer
def Wait(Input):
	CommandString = ""
	CommandString += "[Module]Timer"
	CommandString += "[Command]Wait"
	return CommandString


