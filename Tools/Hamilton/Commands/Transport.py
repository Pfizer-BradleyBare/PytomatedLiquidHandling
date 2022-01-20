from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG

def PreRun(Input):
	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]Transport"
	return CommandString
	
def MoveLabware(Input):
	CommandString = ""
	CommandString += "[Module]Transport"
	CommandString += "[Command]MoveLabware"
	CommandString += "[SourceLabwareType]" + str(Input["SourceLabwareType"]) + "[SourceSequenceString]" + str(Input["SourceSequenceString"]) 
	CommandString += "[DestinationLabwareType]" + str(Input["DestinationLabwareType"]) + "[DestinationSequenceString]" + str(Input["DestinationSequenceString"])
	CommandString += "[Park]" + str(Input["Park"]) + "[CheckExists]" + str(Input["CheckExists"])
	return CommandString


