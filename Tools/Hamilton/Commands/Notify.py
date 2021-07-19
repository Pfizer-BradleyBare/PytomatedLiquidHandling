from ...General import HamiltonIO as HAMILTONIO


#this function will reserve a lid on the Hamilton. This lid can be used on or off the Heaters
def Init():
	CommandString = ""
	CommandString += "[Notify]\n"
	CommandString += "[Init]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	#response is not parsed for this command

#this function will reserve a lid on the Hamilton. This lid can be used on or off the Heaters
def SendMessage(Wait, SubjectString, MessageString):
	CommandString = ""
	CommandString += "[Notify]\n"
	CommandString += "[SendMessage]\n"
	CommandString += "[Wait]" + str(Wait)
	CommandString += "[Subject]" + str(SubjectString)
	CommandString += "[Message]" + str(MessageString) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	#response is not parsed for this command

