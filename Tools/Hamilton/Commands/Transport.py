from ...General import HamiltonIO as HAMILTONIO
	
def Move(SourceSeq, DestinationSeq, OpenDistance, CloseDistance):
	CommandString = ""
	CommandString += "[Transport]\n"
	CommandString += "[Move]\n"
	CommandString += "[Source] " + str(SourceSeq) + "\n"
	CommandString += "[Destination] " + str(DestinationSeq) + "\n"
	CommandString += "[Open] " + str(OpenDistance) + "\n"
	CommandString += "[Close] " + str(CloseDistance) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response



