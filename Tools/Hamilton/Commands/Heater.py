from ...General import HamiltonIO as HAMILTONIO

def StartHeating(ID, Temp):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Start Heat]\n"
	CommandString += "[ID] " + str(ID) + "\n"
	CommandString += "[Temp] " + str(Temp) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StopHeating(ID):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Stop Heat]\n"
	CommandString += "[ID] " + str(ID) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StartShaking(ID, RPM):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Start Shake]\n"
	CommandString += "[ID] " + str(ID) + "\n"
	CommandString += "[RPM] " + str(RPM) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StopShaking(ID):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Stop Shake]\n"
	CommandString += "[ID] " + str(ID) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response






