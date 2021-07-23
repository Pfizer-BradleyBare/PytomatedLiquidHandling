from ...General import HamiltonIO as HAMILTONIO

def PreRun(VolumesArray):
	CommandString = ""
	CommandString += "[PreRun]\n"
	CommandString += "[Pipette]\n" 
	for Volume in VolumesArray:
		CommandString += "[Volume]" + str(Volume) + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

def Do(Dest, Sequences):

	#parameters for a solution transfer command are as follows (NOT ABOVE PARAMETERS)
	#Source: This is where we will aspirate liquid
	#Dest: This is where we will dispense liquid
	#SequenceFactorVolume 2D List: These are the positions, the volume for that position, and the total volume in the container before this step
	#self.Samples.PlateSequenceFactorVolumeAddVolume(Dest, VolumeList)

	Seq = ""
	Vol = ""
	Tot = ""
	Sor = ""
	Mix = ""
	for Sequence in Sequences:
		Seq += str(Sequence[0]) + ","
		Sor += str(Sequence[1]) + ","
		Vol += "{0:.2f}".format(float(Sequence[2])) + ","
		Tot += "{0:.2f}".format(float(Sequence[3])) + ","
		Mix += Sequence[4] + ","

	CommandString = ""
	CommandString += "[Pipette]\n"
	CommandString += "[Destination]" + Dest 
	CommandString += "[Sources]" + Sor[:-1] 
	CommandString += "[Sequences]" + Seq[:-1]
	CommandString += "[Volumes]" + Vol[:-1]  
	CommandString += "[Totals]" + Tot[:-1] 
	CommandString += "[Mix?]" + Mix[:-1] + "\n"

	print(CommandString)

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	#response is not parsed for this command





