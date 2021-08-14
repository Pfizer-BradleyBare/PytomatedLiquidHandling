from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun():
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Notify]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

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

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True
	#response is not parsed for this command

