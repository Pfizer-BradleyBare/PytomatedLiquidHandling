from ...General import HamiltonIO as HAMILTONIO

def PreRun():
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Transport]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	
def Move(SourceSeq, DestinationSeq, OpenDistance, CloseDistance, Eject):
	CommandString = ""
	CommandString += "[Transport]\n"
	CommandString += "[Move]\n"
	CommandString += "[Source]" + str(SourceSeq) + "[Destination]" + str(DestinationSeq) + "[Open]" + str(OpenDistance) + "[Close]" + str(CloseDistance) + "[Eject]" + str(Eject) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response


