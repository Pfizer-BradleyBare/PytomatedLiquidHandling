from ...General import HamiltonIO as HAMILTONIO



#this function will start a timer for a specified plate
def Start(Plate, WaitTime):
	CommandString = ""
	CommandString += "[Timer]\n"
	CommandString += "[Start]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"
	CommandString += "[Time] " + str(WaitTime) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	
#this function will wait on a plate timer
def Wait(Plate):
	CommandString = ""
	CommandString += "[Timer]\n"
	CommandString += "[Wait]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True


