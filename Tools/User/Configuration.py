from ..User.Labware import Plates as PLATES
from ..User.Labware import Solutions as SOLUTIONS
from ..General import ExcelIO as EXCELIO
from ..General import HamiltonIO as HAMILTONIO
import copy
import yaml
import os
import os.path
import collections

#This is a dictionary that contains the loading information
SysConfig = {}
Sequences = {}
PreferredLoading = {}
DeckLoading = {}
StepPreferredLoading = {}
CheckSequences = []

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

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","AutoloadingSequences.yaml"))
	Sequences = yaml.full_load(file)
	file.close()

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","PreferredLoading.yaml"))
	PreferredLoading = yaml.full_load(file)
	file.close()

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","System Configuration.yaml"))
	SysConfig = yaml.full_load(file)
	file.close()

	# if HAMILTONIO.IsSimulated() == False:
	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","Output","DeckLoading.yaml"))
	DeckLoading = yaml.full_load(file)
	file.close()
	# else:
	# 	DeckLoading = None

def WriteLoadingInformation(YamlData):
	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","Output","DeckLoading.yaml"),"w")
	yaml.dump(YamlData,file)
	file.close()


######################################################################### 
#	Description: Returns a list of floats describing well dispense heights 
#	Input Arguments: [PlateName: String], [WellVolumes: List[Float]]
#	Returns: [DispenseHeights: List[float]]
#########################################################################
def WellVolumeToDispenseHeight(PlateName, WellVolumes):
	#use platename to get the  Labware Category, Labware Type, and Max Volume from storage file​	
	#print("Here")
	LabwareLoading = GetDeckLoading(PlateName)
	
	if not LabwareLoading:
		return [0]*len(WellVolumes)
	LabwareCategory =LabwareLoading["Labware Category"]
	LabwareType =LabwareLoading["Labware Type"]
	MaxVolume =LabwareLoading["MaxVolume"]
	Segments = SysConfig["VolumeEquations"][LabwareCategory][LabwareType][MaxVolume]
	print("SEGMENTS = ", Segments)
	Height  = 0
	DispenseHeights = [-1]*len(WellVolumes)

	while(True): 
		Height += .1
		VolumeHeight = VolumeFromHeight(Height,Segments)
		for i in range(0, len(WellVolumes)): 
			if VolumeHeight > WellVolumes[i]:	
				if DispenseHeights[i] == -1:
					DispenseHeights[i] = Height
		if not -1 in DispenseHeights:
			return DispenseHeights

######################################################################### 
#	Description: Calculates Volume from a given height
#	Input Arguments: [Height: Float], [Segments: List[Dict])
#	Returns: [Calculated Volume: Float]
#########################################################################

def VolumeFromHeight(Height, Segments):
	Volume = 0
	for segment in Segments:
		EquationString = segment["SegmentEquation"]
		EquationString = EquationString.replace("x",str(Height))
		Volume += eval(EquationString)
		Height -= float(segment["MaxSegmentHeight"])
		if Height <= 0:
			break
	if Height > 0:
		return float("inf")
	return Volume


######################################################################### 
#	Description: Adds a sequence to the list of sequences to check on the Hamilton devices
#	Input Arguments: [Sequence: String]
#	Returns: N/A
#########################################################################
def AddCheckSequence(Sequence):
	global CheckSequences
	if Sequence not in CheckSequences:
		CheckSequences.append(Sequence)	

######################################################################### 
#	Description: Returns the array of sequences to check
#	Input Arguments: N/A
#	Returns: [1D-array of strings]
#########################################################################
def GetCheckSequences():
	global CheckSequences
	return CheckSequences

######################################################################### 
#	Description: Returns deck loading for a particular labware
#	Input Arguments: [Step: String]
#	Returns: [Dictionary as described in YAML config file]
#########################################################################
def GetDeckLoading(LabwareName):
	global DeckLoading
	if HAMILTONIO.IsSimulated() == True:
		return None
	else:	
		return DeckLoading[LabwareName]


######################################################################### 
#	Description: Returns step specific configuration information
#	Input Arguments: [Step: String]
#	Returns: [Dictionary as described in YAML config file]
#########################################################################
def GetStepConfig(Step):
	global SysConfig
	return SysConfig[Step]

######################################################################### 
#	Description: Returns step specific loading information
#	Input Arguments: [Step: String]
#	Returns: [Dictionary as described in YAML config file]
#########################################################################
def GetStepLoading(Step):
	global PreferredLoading
	return PreferredLoading["Steps"][Step]

######################################################################### 
#	Description: Add software specific loading to dictionary for later processing
#	Input Arguments: [Item: String] [LoadingArray: 1D-Array of strings]
#	Returns: N/A
#########################################################################
def AddPreferredLoading(Item, LoadingArray):
	StepPreferredLoading[Item] = LoadingArray

######################################################################### 
#	Description: Searches for a preferred loading entry for the argument
#	Input Arguments: [LoadingItem: String]
#	Returns: If item is found then returns loading information described in YAML file (Array), else None as array
#########################################################################
def TryPreferred(LoadingItem):
	global PreferredLoading

	for Category in PreferredLoading["Labware"].keys():
		for Item in PreferredLoading["Labware"][Category].keys():
			if Item == LoadingItem:
					return PreferredLoading["Labware"][Category][Item]
	return [None]

######################################################################### 
#	Description: Attempts to load both plates and solutions using the loading information available in the YAML file
#	Input Arguments:  [Plates_List: 1D-array of plate objects] [Solutions_List: 1D-array of solution objects]
#	Returns: If loading was sucessful then returns a dictionary of loading information with item name as key, else returns False
#########################################################################
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
					Temp["Volume"] = MaxVol
					Temp["Max Volume"] = Sequences["Plates"][Sequence]["Max Supported Volume"]
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
				Temp["Max Volume"] = Sequences["Reagents"][Sequence]["Max Supported Volume"]
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
						"Max Volume":Loading[Item]["Sequences"][Sequence]["Max Volume"],
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
						"Max Volume":Loading[Item]["Sequences"][Sequence]["Max Volume"],
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
		if FinalLoading[item]["Labware Category"] == "Plates" and (not not FinalLoading[item]["Lid"]) != False:
			AddCheckSequence(FinalLoading[item]["Lid"])

	return FinalLoading





