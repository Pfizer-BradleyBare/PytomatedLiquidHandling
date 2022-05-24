from ..User.Labware import Labware as LABWARE
from ..General import ExcelIO as EXCELIO
from ..General import HamiltonIO as HAMILTONIO
from ..User import Samples as SAMPLES
import copy
import yaml
import json #this is used for pretty print only
import os
import os.path
import collections

CONFIGURATION_FOLDER = "HamiltonVisualMethodEditorConfiguration\\Configuration"

#This is a dictionary that contains the loading information
SysConfig = {}
Sequences = {}
LabwareInfo = {}
PreferredLoading = {}
OmitLoadingList = []

######################################################################### 
#	Description: Initializes the library by pulling information from Config files
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Init():
	global Sequences
	global PreferredLoading
	global LabwareInfo

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),CONFIGURATION_FOLDER,"AutoloadingSequences.yaml"))
	Sequences = yaml.full_load(file)["Autoloading"]
	file.close()
	
	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),CONFIGURATION_FOLDER,"AutoloadingSequences.yaml"))
	LabwareInfo = yaml.full_load(file)["LabwareInfo"]
	file.close()

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),CONFIGURATION_FOLDER,"PreferredLoading.yaml"))
	PreferredLoading = yaml.full_load(file)
	file.close()

def AddOmitLoading(Item):
	OmitLoadingList.append(Item)

######################################################################### 
#	Description: Attempts to load both plates and solutions using the loading information available in the YAML file
#	Input Arguments:  [Plates_List: 1D-array of plate objects] [Solutions_List: 1D-array of solution objects]
#	Returns: If loading was sucessful then returns a dictionary of loading information with item name as key, else returns False
#########################################################################
def Load(Plates_List, Solutions_List):

	Plates_List = [x for x in Plates_List if LABWARE.Class.GetLabwareName(x) not in OmitLoadingList]

	Loading = {}

	PlateSequences = {k: v for k, v in Sequences.items() if "Plate" == LabwareInfo[v["Labware Name"]]["Labware Category"]}

	for Plate in Plates_List:
		PlateType = Plate.GetPlateType()
		MaxVol = Plate.GetMaxVolume()
		LidRequired = Plate.GetIsCovered()
		VacuumRequired = Plate.GetIsVacuum()
		DesaltRequired = Plate.GetIsIMCSSizeXDesalting()

		Possibles = collections.OrderedDict({k: v for k, v in PlateSequences.items() if 
			LabwareInfo[v["Labware Name"]]["Max Supported Volume"] >= (MaxVol + LabwareInfo[v["Labware Name"]]["Dead Volume"]) and
			PlateType == LabwareInfo[v["Labware Name"]]["Labware Type"] and 
			int(not not v["Lid Sequence"]) >= int(not not LidRequired) and 
			(VacuumRequired == False or VacuumRequired in str(LabwareInfo[v["Labware Name"]]["Vacuum Compatible"])) and
			(DesaltRequired == False or int(not not LabwareInfo[v["Labware Name"]]["IMCS SizeX Desalting Compatible"] >= int( not not DesaltRequired)))})

		Possibles = collections.OrderedDict({k: v for k, v in sorted(Possibles.items(), key=lambda item: LabwareInfo[item[1]["Labware Name"]]["Max Supported Volume"])})

		for item in Possibles:
			Possibles[item]["Used Volume"] = MaxVol + LabwareInfo[Possibles[item]["Labware Name"]]["Dead Volume"]

		Loading[Plate.GetLabwareName()] = {"PreferredCategories":[Plate.GetLabwareName(),Plate.GetPlateType()], "Sequences":collections.OrderedDict(copy.deepcopy(Possibles))}

	ReagentSequences = {k: v for k, v in Sequences.items() if "Reagent" == LabwareInfo[v["Labware Name"]]["Labware Category"]}

	for Solution in Solutions_List:
		SolutionStorage = Solution.GetStorageTemperature()
		MaxVol = Solution.GetMaxVolume()
		DesaltRequired = Solution.GetIsIMCSSizeXDesalting()

		Possibles = {k: v for k, v in ReagentSequences.items() if 
			LabwareInfo[v["Labware Name"]]["Max Supported Volume"] >= (MaxVol + LabwareInfo[v["Labware Name"]]["Dead Volume"]) and 
			SolutionStorage == LabwareInfo[v["Labware Name"]]["Storage Condition"]  and 
			(DesaltRequired == False or int(not not LabwareInfo[v["Labware Name"]]["IMCS SizeX Desalting Compatible"] >= int( not not DesaltRequired)))}

		Possibles = collections.OrderedDict({k: v for k, v in sorted(Possibles.items(), key=lambda item: LabwareInfo[item[1]["Labware Name"]]["Max Supported Volume"])})

		for item in Possibles:
			Possibles[item]["Used Volume"] = MaxVol + LabwareInfo[Possibles[item]["Labware Name"]]["Dead Volume"]

		Loading[Solution.GetLabwareName()] = {"PreferredCategories":[Solution.GetLabwareName(),Solution.GetCategory()], "Sequences":collections.OrderedDict(copy.deepcopy(Possibles))}

	# Do solution loading
	#
	#
	# Our first step is to find all the possible loading candidates for plates and reagents. 
	# We do this by scouring the available sequences and checking correct loading parameters.
	# If everything fits then that sequence is added to our loading dict.
	#
	#
	#

	FinalLoading = {}
	PositionTracker = []

	for Item in Loading:
		done = False
		for PreferredCategory in Loading[Item]["PreferredCategories"]:

			LoadSequences = [None]

			for item in PreferredLoading:
				if item == PreferredCategory:
					LoadSequences = PreferredLoading[item]["Preferred Sequences"]
					break
			
			for Sequence in LoadSequences:
				if Sequence != None and Sequence in Loading[Item]["Sequences"] and Loading[Item]["Sequences"][Sequence]["Deck Position"] not in PositionTracker:
					PositionTracker.append(Loading[Item]["Sequences"][Sequence]["Deck Position"])
					FinalLoading[Item] = {"Sequence":Sequence, 
						"Lid":Loading[Item]["Sequences"][Sequence]["Lid Sequence"], 
						"LoadingPosition":Loading[Item]["Sequences"][Sequence]["Deck Position"], 
						"Used Volume":Loading[Item]["Sequences"][Sequence]["Used Volume"],
						"Labware Name":Loading[Item]["Sequences"][Sequence]["Labware Name"],
						"Labware Info":LabwareInfo[Loading[Item]["Sequences"][Sequence]["Labware Name"]]}
					LoadSequences.remove(Sequence)
					done = True
					break

			if done == True:
				break
		if done == False:
			for Sequence in Loading[Item]["Sequences"]:
				if Loading[Item]["Sequences"][Sequence]["Deck Position"] not in PositionTracker:
					PositionTracker.append(Loading[Item]["Sequences"][Sequence]["Deck Position"])
					FinalLoading[Item] = {"Sequence":Sequence, 
						"Lid":Loading[Item]["Sequences"][Sequence]["Lid Sequence"], 
						"LoadingPosition":Loading[Item]["Sequences"][Sequence]["Deck Position"], 
						"Used Volume":Loading[Item]["Sequences"][Sequence]["Used Volume"],
						"Labware Name":Loading[Item]["Sequences"][Sequence]["Labware Name"],
						"Labware Info":LabwareInfo[Loading[Item]["Sequences"][Sequence]["Labware Name"]]}
					done = True
					break




	#
	#
	#
	# In the final loading step, we check if we can find any of the possible loading positions in the preferred loading config file.
	# if we find one and the position is not already taken, then we load the plate there. If nothing is found, the plate is loaded at the first available possible position
	#
	#
	#

	FinalLoading = dict(sorted(FinalLoading.items(), key=lambda x: x[1]["LoadingPosition"]))
	#Sort by position so the deck loading is in position order

	print(json.dumps(FinalLoading,sort_keys=True, indent=4))

	if(len(Plates_List) + len(Solutions_List) != len(FinalLoading)):
		print("Unabled to load all labware. The following labware exceeds available container volume on deck.")
		for plate in Plates_List:
			if plate.GetLabwareName() not in FinalLoading:
				print(plate.GetLabwareName(),": ",plate.GetMaxVolume())
		for solution in Solutions_List:
			if solution.GetLabwareName() not in FinalLoading:
				print(solution.GetLabwareName(),": ",solution.GetMaxVolume())
		quit()
	#check that we were able to load everything

	return FinalLoading




