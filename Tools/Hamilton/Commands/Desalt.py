from ...General import HamiltonIO as HAMILTONIO


def PreRun(Params):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Desalt]\n"
	CommandString += "[Tips]" + str(Params["Required Tips"])
	CommandString += "[Types]" + str(Params["Type"])
	CommandString += "[Volumes]" + str(Params["Volume"])
	CommandString += "[Source]" + str(Params["Source Sequence"])
	CommandString += "[Buffer]" + str(Params["Buffer Sequence"])
	CommandString += "[Destination]" + str(Params["Destination Sequence"]) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function should start an equilibration on the Hamilton system. If this function is called twice, for whatever reason, the Hamilton should know the tips are equilibrated. 
def Equilibrate():
	CommandString = ""
	CommandString += "[Desalt]\n"
	CommandString += "[Equilibrate]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function should start to process the samples through the desalting tips. The tips are assumed to be equilibrated. It is possible to equilibrate during this step if it hasn't been done yet.
def Process():
	CommandString = ""
	CommandString += "[Desalt]\n"
	CommandString += "[Process]\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True



