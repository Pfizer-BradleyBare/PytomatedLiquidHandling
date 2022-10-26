from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]StatusUpdate"
	return CommandString

#this function will reserve a lid on the Hamilton. This lid can be used on or off the Heaters
def SetProgress(Input):
	CommandString = ""
	CommandString += "[Module]StatusUpdate"
	CommandString += "[Command]SetProgress"
	CommandString += "[PercentComplete]" + str(Input["PercentComplete"])
	return CommandString

def AddProgressDetail(Input):
	CommandString = ""
	CommandString += "[Module]StatusUpdate"
	CommandString += "[Command]AddProgressDetail"
	CommandString += "[DetailMessage]" + str(Input["DetailMessage"])
	return CommandString

def AppendText(text):
	pass