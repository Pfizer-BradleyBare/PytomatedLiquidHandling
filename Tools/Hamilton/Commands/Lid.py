from ...General import HamiltonIO as HAMILTONIO

def PreRun():
	return True

def Init():
	return True

#this function will reserve a lid on the Hamilton. This lid can be used on or off the Heaters
def Reserve(Plate):
	CommandString = ""
	CommandString += "[Lid]\n"
	CommandString += "[Reserve]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	#response is not parsed for this command

#this function will release a lid on the Hamilton.
def Release(Plate):
	CommandString = ""
	CommandString += "[Lid]\n"
	CommandString += "[Release]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will move a lid to the reserved plate location. If the location is on a heater shaker or not the Hamilton should make the proper determination
def Move(Plate):
	CommandString = ""
	CommandString += "[Lid]\n"
	CommandString += "[Move]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will remove the lid and place it back home.
def Remove(Plate):
	CommandString = ""
	CommandString += "[Lid]\n"
	CommandString += "[Remove]\n"
	CommandString += "[Plate] " + str(Plate) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

