from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(VolumesArray):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Pipette" 
	VolumeString = ""
	for Volume in VolumesArray:
		VolumeString += str(Volume) + HAMILTONIO.GetDelimiter()
	CommandString += "[Volume]" + VolumeString[:-1] + "\n"

	HAMILTONIO.Push(CommandString)
	Response = HAMILTONIO.Pull()
	return True

def Transfer(Sequences):

	Dest = ""
	DestPos = ""
	Source = ""
	SourcePos = ""
	Volume = ""
	CurDestVol = ""
	Mix = ""

	for Sequence in Sequences:
		Dest += str(Sequence["Destination"]) + HAMILTONIO.GetDelimiter()
		DestPos += str(Sequence["Destination Position"]) + HAMILTONIO.GetDelimiter()
		Source += str(Sequence["Source"]) + HAMILTONIO.GetDelimiter()
		SourcePos += str(Sequence["Source Position"]) + HAMILTONIO.GetDelimiter()
		Volume += "{0:.2f}".format(float(Sequence["Volume"])) + HAMILTONIO.GetDelimiter()
		CurDestVol += "{0:.2f}".format(float(Sequence["CurrentDestinationVolume"])) + HAMILTONIO.GetDelimiter()
		Mix += Sequence["Mix"] + HAMILTONIO.GetDelimiter()

	CommandString = ""
	CommandString += "[Module]Pipette"
	CommandString += "[Command]Transfer"
	CommandString += "[Destination]" + Dest[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[DestinationPosition]" + DestPos[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[Source]" + Source[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[SourcePosition]" + SourcePos[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[TransferVolume]" + Volume[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[CurrentDestinationVolume]" + CurDestVol[:-1*len(HAMILTONIO.GetDelimiter())]  
	CommandString += "[Mix]" + Mix[:-1*len(HAMILTONIO.GetDelimiter())] + "\n"

	print(CommandString)

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True
	#response is not parsed for this command


def Correct(Sequences):

	#parameters for a solution transfer command are as follows (NOT ABOVE PARAMETERS)
	#Source: This is where we will aspirate liquid
	#Dest: This is where we will dispense liquid
	#SequenceFactorVolume 2D List: These are the positions, the volume for that position, and the total volume in the container before this step
	#self.Samples.PlateSequenceFactorVolumeAddVolume(Dest, VolumeList)

	Dest = ""
	DestPos = ""
	TotalVolume = ""

	for Sequence in Sequences:
		Dest += str(Sequence["Destination"]) + HAMILTONIO.GetDelimiter()
		DestPos += str(Sequence["Destination Position"]) + HAMILTONIO.GetDelimiter()
		TotalVolume += "{0:.2f}".format(float(Sequence["Total"])) + HAMILTONIO.GetDelimiter()

	CommandString = ""
	CommandString += "[Module]Pipette"
	CommandString += "[Command]Correct"
	CommandString += "[Destination]" + Dest[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[DestinationPosition]" + DestPos[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[Total]" + TotalVolume[:-1*len(HAMILTONIO.GetDelimiter())] 

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		HAMILTONIO.Push(CommandString)
		Response = HAMILTONIO.Pull()
		LOG.CommandID()
	return True
	#response is not parsed for this command





