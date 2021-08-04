
from ..Steps import Steps as STEPS
from ..Steps import Liquid_Transfer as LIQUID_TRANSFER
from ..Steps import Dilute as DILUTE
from ..Steps import Desalt as DESALT
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ...User import Configuration as CONFIGURATION

Solutions = {}
Pipette_List = []
Tips_List = {}

STORAGE_AMBIENT = "Ambient"
STORAGE_COLD = "Cold"

TYPE_PLATE = "Plate"
TYPE_REAGENT = "General Reagent"
TYPE_REDUCTANT = "Reductant"
TYPE_ALKYLANT = "Alkylant"
TYPE_QUENCH = "Quench"
TYPE_BUFFER = "Buffer/Diluent"
TYPE_DENATURANT = "Denaturant"
TYPE_ENZYME = "Enzyme"

class Class:
	def __init__(self, Name, Type, Storage):
		self.Name = Name
		self.Type = Type
		self.Storage = Storage
		self.TotalVolume = 0

	def GetName(self):
		return self.Name

	def GetType(self):
		return self.Type

	def GetStorage(self):
		return self.Storage

######################################################################### 
#	Description: Adds volume to the Solution class tracker and to the pipetting list tracker
#	Input Arguments: [Volume: Float]
#	Returns: N/A
#########################################################################
	def AddVolume(self, Volume):
		self.TotalVolume += Volume

	def GetVolume(self):
		return self.TotalVolume

######################################################################### 
#	Description: Sets everything to default value. Add tips configuration information to tracker dictionary
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Init():
	global Solutions
	global Pipette_List
	global Tips_List
	Solutions = {}
	Pipette_List =[]

######################################################################### 
#	Description: Attempts to create and add a solution class to the tracker dictionary
#	Input Arguments: [Solution: String] [Type: String] [Storage: String]
#	Returns: [List of Plate Classes]
#########################################################################
def AddSolution(Solution, Type, Storage):
	global Solutions

	if PLATES.IsPlate(Solution) == True:
		Type = TYPE_PLATE
		Storage = STORAGE_AMBIENT

	try:
		_Temp = Solutions[Solution]
	except:
		Solutions[Solution] = Class(Solution,Type,Storage)

######################################################################### 
#	Description: Returns solution class if it is present in the tracker dictionary
#	Input Arguments: [Solution: String]
#	Returns: If Solution is present in tracker then returns Solution Class object, else None
#########################################################################
def GetSolution(Solution):
	global Solutions
	if Solution in Solutions:
		return Solutions[Solution]
	else:
		return None
		
######################################################################### 
#	Description: Returns all solutions that have a volume greater than 0 and that are not categorized as a plate
#	Input Arguments:  N/A
#	Returns: [List of Solution Objects]
#########################################################################
def GetSolutions():
	global Solutions
	Temp = []
	for key in Solutions:
		if Solutions[key].GetVolume() != 0 and Solutions[key].GetType() != TYPE_PLATE:
			Temp.append(Solutions[key])
	return Temp

def AddPipetteVolume(Volume):
	global Pipette_List
	Pipette_List.append(Volume)

def GetPipetteVolumes():
	global Pipette_List
	return Pipette_List





