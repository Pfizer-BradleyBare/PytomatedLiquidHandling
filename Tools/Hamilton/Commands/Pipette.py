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

def Transfer(Sequences, LiquidClassStrings, TipSequenceStrings):

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
	CommandString += "[Command]TransferLiquid"
	CommandString += "[Destination]" + Dest[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[DestinationPosition]" + DestPos[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[Source]" + Source[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[SourcePosition]" + SourcePos[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[TransferVolume]" + Volume[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[CurrentDestinationVolume]" + CurDestVol[:-1*len(HAMILTONIO.GetDelimiter())]  
	CommandString += "[Mix]" + Mix[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[TipSequence]" + HAMILTONIO.GetDelimiter().join(TipSequenceStrings) #I have to include this for cross module support
	CommandString += "[LiquidClass]" + HAMILTONIO.GetDelimiter().join(LiquidClassStrings) #I have to include this for cross module support
	CommandString += "[KeepTips]" + "True or False"
	return CommandString

def GetLiquidClassStrings(TransferVolumesArray, LiquidCategoriesArray):
	CommandString = ""
	CommandString += "[Module]Pipette"
	CommandString += "[Command]GetLiquidClassStrings"
	CommandString += "[TransferVolume]" + HAMILTONIO.GetDelimiter().join(TransferVolumesArray)
	CommandString += "[LiquidCategory]" + HAMILTONIO.GetDelimiter().join(LiquidCategoriesArray)
	return CommandString

def GetTipSequenceStrings(TransferVolumesArray):
	CommandString = ""
	CommandString += "[Module]Pipette"
	CommandString += "[Command]GetTipSequenceStrings"
	CommandString += "[TransferVolume]" + HAMILTONIO.GetDelimiter().join(TransferVolumesArray)
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





