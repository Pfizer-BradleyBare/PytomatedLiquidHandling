from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun():
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]StatusUpdate"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function will reserve a lid on the Hamilton. This lid can be used on or off the Heaters
def AppendText(MessageString):
	CommandString = ""
	CommandString += "[Module]StatusUpdate"
	CommandString += "[Command]AppendText"
	CommandString += "[Message]" + str(MessageString) + "\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True
####	#response is not parsed for this command
