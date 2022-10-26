from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Labware"


	Names = ""
	LabwareSequences = ""
	LidSequences = ""
	LoadingLocations = ""
	LabwareVolumes = ""
	LabwareTypes = ""
	LabwareCategories = ""
	LabwareNames = ""

	for Labware in Input:
		Names += str(Labware) + HAMILTONIO.GetDelimiter()
		LabwareSequences += str(Input[Labware]["Sequence"]) + HAMILTONIO.GetDelimiter()
		LidSequences += str(Input[Labware]["Lid"]) + HAMILTONIO.GetDelimiter()
		LoadingLocations += str(Input[Labware]["LoadingPosition"]) + HAMILTONIO.GetDelimiter()

		if str(Input[Labware]["Labware Category"]) == "Plates":
			LabwareVolumes += str(Input[Labware]["Max Volume"]) + HAMILTONIO.GetDelimiter()
		else:
			LabwareVolumes += str(Input[Labware]["Volume"]) + HAMILTONIO.GetDelimiter()

		LabwareTypes += str(Input[Labware]["Labware Type"]) + HAMILTONIO.GetDelimiter()
		LabwareCategories += str(Input[Labware]["Labware Category"]) + HAMILTONIO.GetDelimiter()
		LabwareNames += str(Input[Labware]["Labware Name"]) + HAMILTONIO.GetDelimiter()

	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Labware"
	CommandString += "[Name]" + Names[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[LabwareSequence]" + LabwareSequences[:-1*len(HAMILTONIO.GetDelimiter())]
	CommandString += "[LidSequence]" + LidSequences[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[LoadingLocation]" + LoadingLocations[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[Volume]" + LabwareVolumes[:-1*len(HAMILTONIO.GetDelimiter())] 
	CommandString += "[LabwareType]" + LabwareTypes[:-1*len(HAMILTONIO.GetDelimiter())]  
	CommandString += "[LabwareCategory]" + LabwareCategories[:-1*len(HAMILTONIO.GetDelimiter())]  
	CommandString += "[LabwareName]" + LabwareNames[:-1*len(HAMILTONIO.GetDelimiter())] 
	return CommandString
	
def GetSequenceStrings(Input):
	CommandString = ""
	CommandString += "[Module]Labware"
	CommandString += "[Command]GetSequenceStrings"
	CommandString += "[PlateNames]" + HAMILTONIO.GetDelimiter().join(Input["PlateNames"])
	return CommandString

def GetLabwareTypes(Input):
	CommandString = ""
	CommandString += "[Module]Labware"
	CommandString += "[Command]GetLabwareTypes"
	CommandString += "[PlateNames]" + HAMILTONIO.GetDelimiter().join(Input["PlateNames"])
	return CommandString

def GetLidSequenceStrings(Input):
	CommandString = ""
	CommandString += "[Module]Labware"
	CommandString += "[Command]GetLidSequenceStrings"
	CommandString += "[PlateNames]" + HAMILTONIO.GetDelimiter().join(Input["PlateNames"])
	return CommandString

