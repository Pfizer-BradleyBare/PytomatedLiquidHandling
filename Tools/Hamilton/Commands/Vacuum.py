from ...General import HamiltonIO as HAMILTONIO

def PreRun(ID):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Vacuum]\n"
	CommandString += "[ID]" + str(ID) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will start a timer for a specified plate
def Start(Pressure, Time):
	CommandString = ""
	CommandString += "[Vacuum]\n"
	CommandString += "[Start]\n"
	CommandString += "[Pressure]" + str(Pressure) + "[Time]" + str(Time) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	
#this function will wait on a plate timer
def Wait():
	CommandString = ""
	CommandString += "[Vaccum]\n"
	CommandString += "[Wait]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True


