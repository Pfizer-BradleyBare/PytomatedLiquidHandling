from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG


def PreRun(Params):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Desalt"
	CommandString += "[Tips]" + str(Params["Required Tips"])
	CommandString += "[Types]" + str(Params["Type"]).replace(",",HAMILTONIO.GetDelimiter())
	CommandString += "[Volumes]" + str(Params["Volume"]).replace(",",HAMILTONIO.GetDelimiter())
	CommandString += "[Source]" + str(Params["Source Sequence"])
	CommandString += "[Buffer]" + str(Params["Buffer Sequence"])
	CommandString += "[Waste]" + str(Params["Waste Sequence"])
	CommandString += "[Destination]" + str(Params["Destination Sequence"])
	return CommandString

#this function should start an equilibration on the Hamilton system. If this function is called twice, for whatever reason, the Hamilton should know the tips are equilibrated. 
def Equilibrate():
	CommandString = ""
	CommandString += "[Module]Desalt"
	CommandString += "[Command]Equilibrate"
	return CommandString

#this function should start to process the samples through the desalting tips. The tips are assumed to be equilibrated. It is possible to equilibrate during this step if it hasn't been done yet.
def Process():
	CommandString = ""
	CommandString += "[Module]Desalt"
	CommandString += "[Command]Process"
	return CommandString



