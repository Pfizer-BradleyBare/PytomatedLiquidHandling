from ...General import HamiltonIO as HAMILTONIO


def PreRun(Tips, SampleVolume):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Desalt]\n"
	CommandString += "[Tips] " + str(Tips)
	CommandString += "[Volume] " + str(SampleVolume) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function should start an equilibration on the Hamilton system. If this function is called twice, for whatever reason, the Hamilton should know the tips are equilibrated. 
def Equilibrate(Buffer, Volume):
	CommandString = ""
	CommandString += "[Desalt]\n"
	CommandString += "[Equilibrate]\n"
	CommandString += "[Buffer] " + str(Buffer)
	CommandString += "[Volume] " + str(Volume) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

#this function should start to process the samples through the desalting tips. The tips are assumed to be equilibrated. It is possible to equilibrate during this step if it hasn't been done yet.
def Process(Destination, Source, Buffer, Volume):
	CommandString = ""
	CommandString += "[Desalt]\n"
	CommandString += "[Process]\n"
	CommandString += "[Buffer] " + str(Buffer)
	CommandString += "[Volume] " + str(Volume)
	CommandString += "[Source] " + str(Source) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True



