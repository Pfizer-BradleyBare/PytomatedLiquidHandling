from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(StepDict):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Log" 
	CommandString += "[Title]" + StepDict["Title"] + "[Coordinates]" + StepDict["Coordinates"] + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def Do():
	pass





