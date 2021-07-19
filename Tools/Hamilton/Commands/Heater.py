from ...General import HamiltonIO as HAMILTONIO

def PreRun():
	return True

def Init(HeaterList):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Init]\n"
	for Heater in HeaterList:
		CommandString += "[ID]" + str(Heater["ID"]) + "[Type]" + str(Heater["Type"]) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StartHeating(ID, Temp):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Start Heat]\n"
	CommandString += "[ID]" + str(ID) + "[Temp]" + str(Temp) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StopHeating(ID):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Stop Heat]\n"
	CommandString += "[ID]" + str(ID) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StartShaking(ID, RPM):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Start Shake]\n"
	CommandString += "[ID]" + str(ID) + "[RPM]" + str(RPM) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StopShaking(ID):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Stop Shake]\n"
	CommandString += "[ID]" + str(ID) + "\n"
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response






