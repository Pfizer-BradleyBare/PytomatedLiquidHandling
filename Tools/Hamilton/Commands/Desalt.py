from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG


def PreRun(Input):
	print("Begin")

	CommandString = ""
	CommandString += "[Module]PreRun"
	CommandString += "[Command]IMCS SizeX Desalt"
	CommandString += "[Parents]" + HAMILTONIO.GetDelimiter().join([str(key) for key in Input])
	CommandString += "[Destination]" + HAMILTONIO.GetDelimiter().join([str(Input[key]["Destination"]) for key in Input])
	CommandString += "[Source]" + HAMILTONIO.GetDelimiter().join([str(Input[key]["Source"]) for key in Input])
	CommandString += "[Waste]" + HAMILTONIO.GetDelimiter().join([str(Input[key]["Waste"]) for key in Input])
	CommandString += "[Buffer]" + HAMILTONIO.GetDelimiter().join([str(Input[key]["EQ Buffer"]) for key in Input])
	CommandString += "[Volume]" + HAMILTONIO.GetDelimiter().join([str(",".join(map(str,Input[key]["Volume"]))) for key in Input])
	CommandString += "[Method]" + HAMILTONIO.GetDelimiter().join([str(Input[key]["Method"]) for key in Input])
	CommandString += "[Positions]" + HAMILTONIO.GetDelimiter().join([str(",".join(map(str,Input[key]["Positions"]))) for key in Input])
	return CommandString

#this function should start an equilibration on the Hamilton system. If this function is called twice, for whatever reason, the Hamilton should know the tips are equilibrated. 
def Equilibrate(Input):
	CommandString = ""
	CommandString += "[Module]IMCS SizeX Desalt"
	CommandString += "[Command]Equilibrate"
	CommandString += "[Parent]" + Input["ParentPlate"] + "[StartPosition]" + str(Input["StartPosition"])
	return CommandString

#this function should start to process the samples through the desalting tips. The tips are assumed to be equilibrated. It is possible to equilibrate during this step if it hasn't been done yet.
def Process(Input):
	CommandString = ""
	CommandString += "[Module]IMCS SizeX Desalt"
	CommandString += "[Command]Process"
	CommandString += "[Parent]" + Input["ParentPlate"] + "[StartPosition]" + str(Input["StartPosition"])
	return CommandString



