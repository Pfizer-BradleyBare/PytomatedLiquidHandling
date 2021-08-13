from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

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

	Dest = ""
	DestPos = ""
	Source = ""
	SourcePos = ""
	Volume = ""
	DestHeight = ""
	TotalVolume = ""
	Mix = ""

	for Sequence in Sequences:
		Dest += str(Sequence["Destination"]) + ","
		DestPos += str(Sequence["Destination Position"]) + ","
		Source += str(Sequence["Source"]) + ","
		SourcePos += str(Sequence["Source Position"]) + ","
		Volume += "{0:.2f}".format(float(Sequence["Volume"])) + ","
		DestHeight += "{0:.2f}".format(float(Sequence["Height"])) + ","
		TotalVolume += "{0:.2f}".format(float(Sequence["Total"])) + ","
		Mix += Sequence["Mix"] + ","

	CommandString = ""
	CommandString += "[Pipette]\n"
	CommandString += "[Destination]" + Dest[:-1]
	CommandString += "[DestinationPosition]" + DestPos[:-1]
	CommandString += "[Source]" + Source[:-1] 
	CommandString += "[SourcePosition]" + SourcePos[:-1] 
	CommandString += "[TransferVolume]" + Volume[:-1] 
	CommandString += "[DestinationHeight]" + DestHeight[:-1]  
	CommandString += "[Total]" + TotalVolume[:-1] 
	CommandString += "[Mix]" + Mix[:-1] + "\n"

	LOG.Command(CommandString)

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True
	#response is not parsed for this command





