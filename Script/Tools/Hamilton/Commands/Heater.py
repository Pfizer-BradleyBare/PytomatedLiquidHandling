from ...General import HamiltonIO as HAMILTONIO

def PreRun(HeaterList):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Heater]\n"
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

	print(CommandString)

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StopHeating(ID):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Stop Heat]\n"
	CommandString += "[ID]" + str(ID) + "\n"

	print(CommandString)

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StartShaking(ID, RPM):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Start Shake]\n"
	CommandString += "[ID]" + str(ID) + "[RPM]" + str(RPM) + "\n"

	print(CommandString)

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response

def StopShaking(ID):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Stop Shake]\n"
	CommandString += "[ID]" + str(ID) + "\n"

	print(CommandString)
	
	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return Response






