from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun():
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Transport"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	
def Move(SourceSeq, DestinationSeq, OpenDistance, CloseDistance, GripHeight, Eject, Check):
	CommandString = ""
	CommandString += "[Module]Transport"
	CommandString += "[Command]Move"
	CommandString += "[Source]" + str(SourceSeq) + "[Destination]" + str(DestinationSeq) + "[Open]" + str(OpenDistance) + "[Close]" + str(CloseDistance) + "[Grip]" + str(GripHeight) + "[Eject]" + str(Eject) + "[Check]" + str(Check) + "\n"
	
	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True


