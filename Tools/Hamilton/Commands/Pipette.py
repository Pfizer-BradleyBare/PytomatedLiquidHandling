from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(VolumesArray):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Pipette" 
	VolumeString = ""
	for Volume in VolumesArray:
		VolumeString += str(Volume) + HAMILTONIO.GetDelimiter()
	CommandString += "[Volume]" + VolumeString[:-1*len(HAMILTONIO.GetDelimiter())]
	return CommandString

def Transfer(Input):
	CommandString = ""
	CommandString += "[Module]Pipette"
	CommandString += "[Command]TransferLiquid"
	CommandString += "[Destination]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SequenceClass"].GetDestinations()])
	CommandString += "[DestinationPosition]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SequenceClass"].GetDestinationPositions()])
	CommandString += "[Source]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SequenceClass"].GetSources()])
	CommandString += "[SourcePosition]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SequenceClass"].GetSourcePositions()])
	CommandString += "[TransferVolume]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SequenceClass"].GetTransferVolumes()])
	CommandString += "[CurrentDestinationVolume]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SequenceClass"].GetCurrentDestinationVolumes()])
	CommandString += "[AspirateMix]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SequenceClass"].GetAspirateCycles()])
	CommandString += "[DispenseMix]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SequenceClass"].GetDispenseCycles()])
	CommandString += "[TipSequence]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["TipSequences"]]) #I have to include this for cross module support
	CommandString += "[SourceLiquidClass]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["SourceLiquidClasses"]]) #I have to include this for cross module support
	CommandString += "[DestinationLiquidClass]" + HAMILTONIO.GetDelimiter().join([str(item) for item in Input["DestinationLiquidClasses"]]) #I have to include this for cross module support
	CommandString += "[DestinationPipettingOffset]" + str(Input["DestinationPipettingOffset"])
	CommandString += "[KeepTips]" + str(Input["KeepTips"]) #If True, the command will assume that tips are on an isolated rack (Tip support rack or similar)
	return CommandString

def GetLiquidClassStrings(Input):
	CommandString = ""
	CommandString += "[Module]Pipette"
	CommandString += "[Command]GetLiquidClassStrings"
	CommandString += "[TransferVolume]" + HAMILTONIO.GetDelimiter().join([str(vol) for vol in Input["TransferVolumes"]])
	CommandString += "[LiquidCategory]" + HAMILTONIO.GetDelimiter().join(Input["LiquidCategories"])
	return CommandString

def GetTipSequenceStrings(Input):
	CommandString = ""
	CommandString += "[Module]Pipette"
	CommandString += "[Command]GetTipSequenceStrings"
	CommandString += "[TransferVolume]" + HAMILTONIO.GetDelimiter().join([str(vol) for vol in Input["TransferVolumes"]])
	return CommandString

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
	return CommandString





