from ...General import HamiltonIO as HAMILTONIO

def PreRun():
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Transport]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	
def Move(SourceSeq, DestinationSeq, OpenDistance, CloseDistance):
	CommandString = ""
	CommandString += "[Transport]\n"
	CommandString += "[Move]\n"
	CommandString += "[Source]" + str(SourceSeq) + "[Destination]" + str(DestinationSeq) + "[Open]" + str(OpenDistance) + "[Close]" + str(CloseDistance) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def HeaterMove(PlateSource, PlateDest, PlateOpen, PlateClose, LidSource, LidDest, LidOpen, LidClose):
	CommandString = ""
	CommandString += "[Transport]\n"
	CommandString += "[Heater Move]\n"
	CommandString += "[PlateSource]" + str(PlateSource) + "[PlateDest]" + str(PlateDest) + "[PlateOpen]" + str(PlateOpen) + "[PlateClose]" + str(PlateClose)
	CommandString += "[LidSource]" + str(LidSource) + "[LidDest]" + str(LidDest) + "[LidOpen]" + str(LidOpen) + "[LidClose]" + str(LidClose) +"\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def HeaterRemove(PlateSource, PlateDest, PlateOpen, PlateClose, LidSource, LidDest, LidOpen, LidClose):
	CommandString = ""
	CommandString += "[Transport]\n"
	CommandString += "[Heater Remove]\n"
	CommandString += "[PlateSource]" + str(PlateSource) + "[PlateDest]" + str(PlateDest) + "[PlateOpen]" + str(PlateOpen) + "[PlateClose]" + str(PlateClose)
	CommandString += "[LidSource]" + str(LidSource) + "[LidDest]" + str(LidDest) + "[LidOpen]" + str(LidOpen) + "[LidClose]" + str(LidClose) +"\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response




