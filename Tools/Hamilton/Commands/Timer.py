from ...General import HamiltonIO as HAMILTONIO

def PreRun():
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Timer]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will start a timer for a specified plate
def Start(WaitTime):
	CommandString = ""
	CommandString += "[Timer]\n"
	CommandString += "[Start]\n"
	CommandString += "[Time]" + str(WaitTime) + "\n"

	print(CommandString)

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	
#this function will wait on a plate timer
def Wait():
	CommandString = ""
	CommandString += "[Timer]\n"
	CommandString += "[Wait]\n"

	print(CommandString)

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True


