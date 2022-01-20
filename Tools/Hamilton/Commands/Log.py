from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Log" 
	CommandString += "[Title]" + Input["Title"] + "[Coordinates]" + Input["Coordinates"]
	return CommandString

def Do(Input):
	pass





