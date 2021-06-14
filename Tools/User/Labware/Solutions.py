
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

	def AddVolume(self, Volume):
		self.TotalVolume += Volume
		global Pipette_List
		Pipette_List.append(Volume)

	def GetVolume(self):
		return self.TotalVolume

def AddSolution(Solution, Type, Storage):
	global Solutions

	if PLATES.IsPlate(Solution) == True:
		Type = TYPE_PLATE
		Storage = STORAGE_AMBIENT

	try:
		_Temp = Solutions[Solution]
	except:
		Solutions[Solution] = Class(Solution,Type,Storage)

def GetSolution(Solution):
	global Solutions
	if Solution in Solutions:
		return Solutions[Solution]
	else:
		return None
		
def Init():
	global Solutions
	global Pipette_List
	global Tips_List
	Solutions = {}
	Pipette_List =[]

	Config = CONFIGURATION.GetStepConfig("Tips")

	for Tip in Config:
		Tips_List[Tip] = Config[Tip]
		Tips_List[Tip]["Used"] = 0

def GetSolutions():
	global Solutions
	Temp = []
	for key in Solutions:
		if Solutions[key].GetVolume() > 0 and Solutions[key].GetType() != TYPE_PLATE:
			Temp.append(Solutions[key])
	return Temp

def GetPipetteVolumes():
	global Pipette_List
	return Pipette_List

def GetPipetteTips():
	global Pipette_List
	global Tips_List

	Vols = []

	for Tip in Tips_List:
		Vols.append([Tips_List[Tip]["Max Volume"], Tip])

	Vols = sorted(Vols, key = lambda l:l[0])
	#Get possible tip sizes in order from least to greatest

	for vol in Pipette_List:
		for TipVol in Vols:
			if vol <= TipVol[0]:
				Tips_List[TipVol[1]]["Used"] += 1
				break 

	return Tips_List



