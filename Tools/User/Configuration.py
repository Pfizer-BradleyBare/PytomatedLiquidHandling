from ..User.Labware import Plates as PLATES
from ..User.Labware import Solutions as SOLUTIONS
from ..General import ExcelIO as EXCELIO
import copy
import yaml
import os
import collections

#This is a dictionary that contains the loading information
SysConfig = {}
Sequences = {}
PreferredLoading = {}
StepPreferredLoading = {}
CheckSequences = []

def Init():
	global Sequences
	global PreferredLoading
	global SysConfig

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","AutoloadingSequences.yaml"))
	Sequences = yaml.full_load(file)
	file.close()

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","PreferredLoading.yaml"))
	PreferredLoading = yaml.full_load(file)
	file.close()

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","System Configuration.yaml"))
	SysConfig = yaml.full_load(file)
	file.close()

def AddCheckSequence(Sequence):
	global CheckSequences
	if Sequence not in CheckSequences:
		CheckSequences.append(Sequence)	

def GetCheckSequences():
	global CheckSequences
	return CheckSequences

def GetStepConfig(Step):
	global SysConfig
	return SysConfig[Step]

def GetStepLoading(Step):
	global PreferredLoading
	return PreferredLoading["Steps"][Step]

def AddPreferredLoading(Item, LoadingArray):
	StepPreferredLoading[Item] = LoadingArray

def TryPreferred(LoadingItem):
	global PreferredLoading

	for Category in PreferredLoading["Labware"].keys():
		for Item in PreferredLoading["Labware"][Category].keys():
			if Item == LoadingItem:
					return PreferredLoading["Labware"][Category][Item]
	return [None]



def Load(Plates_List, Solutions_List):
	global Sequences
	global StepPreferredLoading
	global SysConfig

	Loading = {}

	for Plate in Plates_List:

		PlateType = Plate.GetType()
		MaxVol = Plate.GetVolume()
		LidRequired = Plate.GetLidState()
		
		Possibles = {}

		for Sequence in Sequences["Plates"]:
			if Sequences["Plates"][Sequence]["Max Supported Volume"] >= MaxVol:
				if int(not not Sequences["Plates"][Sequence]["Lid"]) >= int(not not LidRequired):
					Temp = {}
					Temp["Volume"] = Sequences["Plates"][Sequence]["Max Supported Volume"]
					Temp["Labware Type"] = Sequences["Plates"][Sequence]["Labware Type"]
					Temp["Labware Category"] = "Plates"
					Temp["Lid"] = Sequences["Plates"][Sequence]["Lid"]
					Temp["Deck Position"] = Sequences["Plates"][Sequence]["Deck Position"]
					Possibles = {**Possibles, **{Sequence:Temp}}
		Loading[Plate.GetName()] = {"PreferredCategories":[Plate.GetName(),Plate.GetType()], "Sequences":copy.deepcopy(Possibles)}

	SolutionDeadVolumes = SysConfig["Dead Volume"]["Reagents"]
	for Solution in Solutions_List:
		SolutionStorage = Solution.GetStorage()
		MaxVol = Solution.GetVolume()

		Possibles = {}

		for Sequence in Sequences["Reagents"]:
			if Sequences["Reagents"][Sequence]["Labware Type"] in SolutionDeadVolumes:
				MaxVolWDead = SolutionDeadVolumes[Sequences["Reagents"][Sequence]["Labware Type"]] + MaxVol

			if Sequences["Reagents"][Sequence]["Max Supported Volume"] >= MaxVolWDead and Sequences["Reagents"][Sequence]["Storage Condition"] == SolutionStorage:
				Temp = {}
				Temp["Volume"] = MaxVolWDead
				Temp["Labware Type"] = Sequences["Reagents"][Sequence]["Labware Type"]
				Temp["Labware Category"] = "Reagents"
				Temp["Lid"] = Sequences["Reagents"][Sequence]["Lid"]
				Temp["Deck Position"] = Sequences["Reagents"][Sequence]["Deck Position"]
				Possibles = {**Possibles, **{Sequence:Temp}}
		Loading[Solution.GetName()] = {"PreferredCategories":[Solution.GetName(),Solution.GetType()], "Sequences":copy.deepcopy(Possibles)}

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
			LoadSequences = TryPreferred(PreferredCategory)
			if Item in StepPreferredLoading:
				LoadSequences = StepPreferredLoading[Item] + LoadSequences
			
			for Sequence in LoadSequences:
				if Sequence != None and Sequence in Loading[Item]["Sequences"] and Loading[Item]["Sequences"][Sequence]["Deck Position"] not in PositionTracker:
				
					PositionTracker.append(Loading[Item]["Sequences"][Sequence]["Deck Position"])
					FinalLoading[Item] = {"Sequence":Sequence, 
						"Lid":Loading[Item]["Sequences"][Sequence]["Lid"], 
						"LoadingPosition":Loading[Item]["Sequences"][Sequence]["Deck Position"], 
						"Volume":Loading[Item]["Sequences"][Sequence]["Volume"],
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
						"Lid":Loading[Item]["Sequences"][Sequence]["Lid"], 
						"LoadingPosition":Loading[Item]["Sequences"][Sequence]["Deck Position"], 
						"Volume":Loading[Item]["Sequences"][Sequence]["Volume"],
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

	if(len(Plates_List) + len(Solutions_List) != len(FinalLoading)):
		return False
	#check that we were able to load everything

	global CheckSequences

	for item in FinalLoading:
		AddCheckSequence(FinalLoading[item]["Sequence"])

	return FinalLoading





