from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG


def PreRun(Params):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Desalt]\n"
	CommandString += "[Tips]" + str(Params["Required Tips"])
	CommandString += "[Types]" + str(Params["Type"]).replace(",",HAMILTONIO.GetDelimiter())
	CommandString += "[Volumes]" + str(Params["Volume"]).replace(",",HAMILTONIO.GetDelimiter())
	CommandString += "[Source]" + str(Params["Source Sequence"])
	CommandString += "[Buffer]" + str(Params["Buffer Sequence"])
	CommandString += "[Waste]" + str(Params["Waste Sequence"])
	CommandString += "[Destination]" + str(Params["Destination Sequence"]) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function should start an equilibration on the Hamilton system. If this function is called twice, for whatever reason, the Hamilton should know the tips are equilibrated. 
def Equilibrate():
	CommandString = ""
	CommandString += "[Desalt]\n"
	CommandString += "[Equilibrate]\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True

#this function should start to process the samples through the desalting tips. The tips are assumed to be equilibrated. It is possible to equilibrate during this step if it hasn't been done yet.
def Process():
	CommandString = ""
	CommandString += "[Desalt]\n"
	CommandString += "[Process]\n"

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True



