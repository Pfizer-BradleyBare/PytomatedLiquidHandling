from ...General import HamiltonIO as HAMILTONIO
	
#this function should be implemented to check if a heater is available with the below specifications then start heating.
#The Hamilton should only support 1 reservation per plate.
def Reserve(Plate, Temp, RPM):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Reserve]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"
	CommandString += "[Temp] " + str(Temp) + "\n"
	CommandString += "[RPM] " + str(RPM) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()

	if Response != None and "True".lower() in Response.lower():
		return True
	else:
		return False
	#response is not parsed for this command

#this function will stop plate heating and release the hold
def Release(Plate):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Release]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function should move the plate to the heater and start shaking if it is required and supported
def Move(Plate):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Move]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function should stop shaking then remove the plate from the heater
def Remove(Plate):
	CommandString = ""
	CommandString += "[Heater]\n"
	CommandString += "[Remove]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True




