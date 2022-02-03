from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]MagneticBeads"
	CommandString += "[PlateNames]" + HAMILTONIO.GetDelimiter().join(Input["PlateNames"])
	return CommandString

def GetCondensedBeadsLiquidClassStrings(Input):
	CommandString = ""
	CommandString += "[Module]MagneticBeads"
	CommandString += "[Command]GetCondensedBeadsLiquidClassStrings"
	CommandString += "[PlateName]" + str(Input["PlateName"]) + "[TransferVolumes]" + HAMILTONIO.GetDelimiter().join([str(vol) for vol in Input["TransferVolumes"]])
	return CommandString

def GetGeneralLiquidTransferLiquidClassStrings(Input):
	CommandString = ""
	CommandString += "[Module]MagneticBeads"
	CommandString += "[Command]GetGeneralLiquidTransferLiquidClassStrings"
	CommandString += "[PlateName]" + str(Input["PlateName"]) + "[TransferVolumes]" + HAMILTONIO.GetDelimiter().join([str(vol) for vol in Input["TransferVolumes"]])
	return CommandString

def GetMagneticRackPlateSequenceString(Input):
	CommandString = ""
	CommandString += "[Module]MagneticBeads"
	CommandString += "[Command]GetMagneticRackPlateSequenceString"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString

def GetMagneticRackPlateTransportType(Input):
	CommandString = ""
	CommandString += "[Module]MagneticBeads"
	CommandString += "[Command]GetMagneticRackPlateTransportType"
	CommandString += "[PlateName]" + str(Input["PlateName"])
	return CommandString







