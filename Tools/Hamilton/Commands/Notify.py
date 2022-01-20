from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Notify"
	return CommandString

#this function will reserve a lid on the Hamilton. This lid can be used on or off the Heaters
def NotifyContacts(Input):
	CommandString = ""
	CommandString += "[Module]Notify"
	CommandString += "[Command]NotifyContacts"
	CommandString += "[Subject]" + str(Input["Subject"])
	CommandString += "[Body]" + str(Input["Body"])
	return CommandString
	#response is not parsed for this command

