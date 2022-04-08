from ..User.Labware import Plates as PLATES
from ..User.Labware import Solutions as SOLUTIONS
from ..General import ExcelIO as EXCELIO
from ..General import HamiltonIO as HAMILTONIO
from ..User import Samples as SAMPLES
import copy
import yaml
import os
import os.path
import collections

CONFIGURATION_FOLDER = "HamiltonVisualMethodEditorConfiguration\\Configuration"

#This is a dictionary that contains the loading information
SysConfig = {}
Sequences = {}
PreferredLoading = {}
StepPreferredLoading = {}
OmitLoadingList = []

######################################################################### 
#	Description: Initializes the library by pulling information from Config files
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Init():
	global Sequences
	global PreferredLoading
	global SysConfig
	global DeckLoading

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),CONFIGURATION_FOLDER,"AutoloadingSequences.yaml"))
	Sequences = yaml.full_load(file)
	file.close()

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),CONFIGURATION_FOLDER,"PreferredLoading.yaml"))
	PreferredLoading = yaml.full_load(file)
	file.close()

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),CONFIGURATION_FOLDER,"System Configuration.yaml"))
	SysConfig = yaml.full_load(file)
	file.close()

def GetSysConfig():
	global SysConfig	
	return SysConfig	

def GetAutoloadingSequences():
	global Sequences
	return Sequences

######################################################################### 
#	Description: Returns step specific configuration information
#	Input Arguments: [Step: String]
#	Returns: [Dictionary as described in YAML config file]
#########################################################################
def GetStepConfig(Step):
	global SysConfig
	return SysConfig["Steps"][Step]

######################################################################### 
#	Description: Add software specific loading to dictionary for later processing
#	Input Arguments: [Item: String] [LoadingArray: 1D-Array of strings]
#	Returns: N/A
#########################################################################
def AddPreferredLoading(Item, LoadingArray):
	global StepPreferredLoading
	StepPreferredLoading[Item] = LoadingArray

def AddOmitLoading(Item):
	global OmitLoadingList
	OmitLoadingList.append(Item)

######################################################################### 
#	Description: Attempts to load both plates and solutions using the loading information available in the YAML file
#	Input Arguments:  [Plates_List: 1D-array of plate objects] [Solutions_List: 1D-array of solution objects]
#	Returns: If loading was sucessful then returns a dictionary of loading information with item name as key, else returns False
#########################################################################
def Load(Plates_List, Solutions_List):
	global Sequences
	global StepPreferredLoading
	global SysConfig
	global PreferredLoading
	global OmitLoadingList

	Plates_List = [x for x in Plates_List if x.GetName() not in OmitLoadingList]

	Loading = {}

	PlateSequences = {k: v for k, v in Sequences.items() if "Plate" == v["Labware Category"]}

	for Plate in Plates_List:
		PlateType = Plate.GetType()
		MaxVol = Plate.GetVolume()
		LidRequired = Plate.GetLidState()
		VacuumRequired = Plate.GetVacuumState()

		Possibles = collections.OrderedDict({k: v for k, v in PlateSequences.items() if v["Max Supported Volume"] >= (MaxVol + v["Dead Volume"]) and PlateType == v["Labware Type"] and int(not not v["Lid Sequence"]) >= int(not not LidRequired) and (VacuumRequired == False or VacuumRequired in str(v["Vacuum Compatible"]))})
		Possibles = collections.OrderedDict({k: v for k, v in sorted(Possibles.items(), key=lambda item: item[1]["Max Supported Volume"])})

		for item in Possibles:
			Possibles[item]["Used Volume"] = MaxVol + Possibles[item]["Dead Volume"]

		Loading[Plate.GetName()] = {"PreferredCategories":[Plate.GetName(),Plate.GetType()], "Sequences":collections.OrderedDict(copy.deepcopy(Possibles))}

	ReagentSequences = {k: v for k, v in Sequences.items() if "Reagent" == v["Labware Category"]}

	for Solution in Solutions_List:
		SolutionStorage = Solution.GetStorage()
		MaxVol = Solution.GetVolume()

		Possibles = {k: v for k, v in ReagentSequences.items() if v["Max Supported Volume"] >= (MaxVol + v["Dead Volume"]) and SolutionStorage == v["Storage Condition"]}
		Possibles = collections.OrderedDict({k: v for k, v in sorted(Possibles.items(), key=lambda item: item[1]["Max Supported Volume"])})

		for item in Possibles:
			Possibles[item]["Used Volume"] = MaxVol + Possibles[item]["Dead Volume"]

		Loading[Solution.GetName()] = {"PreferredCategories":[Solution.GetName(),Solution.GetType()], "Sequences":collections.OrderedDict(copy.deepcopy(Possibles))}

	# Do solution loading
	#
	#
	# Our first step is to find all the possible loading candidates for plates and reagents. 
	# We do this by scouring the available sequences and checking correct loading parameters.
	# If everything fits then that sequence is added to our loading dict.
	#
	#
	#

	Loading = collections.OrderedDict(Loading)
	for Item in StepPreferredLoading.keys():
		Loading.move_to_end(Item, False)
	#Make sure that step specific loading is always done first

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

			if Item in StepPreferredLoading:
				LoadSequences = StepPreferredLoading[Item] + LoadSequences
			
			for Sequence in LoadSequences:
				if Sequence != None and Sequence in Loading[Item]["Sequences"] and Loading[Item]["Sequences"][Sequence]["Deck Position"] not in PositionTracker:
				
					PositionTracker.append(Loading[Item]["Sequences"][Sequence]["Deck Position"])
					FinalLoading[Item] = {"Sequence":Sequence, 
						"Lid":Loading[Item]["Sequences"][Sequence]["Lid Sequence"], 
						"LoadingPosition":Loading[Item]["Sequences"][Sequence]["Deck Position"], 
						"Max Volume":Loading[Item]["Sequences"][Sequence]["Max Supported Volume"],
						"Volume":Loading[Item]["Sequences"][Sequence]["Used Volume"],
						"Labware Name":Loading[Item]["Sequences"][Sequence]["Labware Name"],
						"Labware Type":Loading[Item]["Sequences"][Sequence]["Labware Type"],
						"Labware Category":Loading[Item]["Sequences"][Sequence]["Labware Category"]}
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
						"Max Volume":Loading[Item]["Sequences"][Sequence]["Max Supported Volume"],
						"Volume":Loading[Item]["Sequences"][Sequence]["Used Volume"],
						"Labware Name":Loading[Item]["Sequences"][Sequence]["Labware Name"],
						"Labware Type":Loading[Item]["Sequences"][Sequence]["Labware Type"],
						"Labware Category":Loading[Item]["Sequences"][Sequence]["Labware Category"]}
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

	if(len(Plates_List) + len(Solutions_List) != len(FinalLoading)):
		print("Unabled to load all labware. The following labware exceeds available container volume on deck.")
		for plate in Plates_List:
			if plate.GetName() not in FinalLoading:
				print(plate.GetName(),": ",plate.GetVolume())
		for solution in Solutions_List:
			if solution.GetName() not in FinalLoading:
				print(solution.GetName(),": ",solution.GetVolume())
		quit()
	#check that we were able to load everything

	return FinalLoading




