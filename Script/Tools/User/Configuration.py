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

	if HAMILTONIO.IsSimulated() == False:
		file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","Output","DeckLoading.yaml"))
		DeckLoading = yaml.full_load(file)
		file.close()
	else:
	 	DeckLoading = None

def WriteLoadingInformation(YamlData):
	global DeckLoading

	file  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Configuration","Output","DeckLoading.yaml"),"w")
	yaml.dump(YamlData,file)
	file.close()
	DeckLoading = YamlData



######################################################################### 
#	Description: Returns a list of floats describing well dispense heights 
#	Input Arguments: [PlateName: String], [WellVolumes: List[Float]]
#	Returns: [DispenseHeights: List[float]]
#########################################################################
def WellVolumeToDispenseHeight(PlateName, WellVolumes):
	HEIGHT_INCREMENT = 0.01

	#use platename to get the  Labware Category, Labware Type, and Max Volume from storage file​	
	LabwareLoading = GetDeckLoading(PlateName)

	if not LabwareLoading:
		return [0]*len(WellVolumes)

	Segments = SysConfig["VolumeEquations"][LabwareLoading["Labware Name"]]
	Height  = 0
	DispenseHeights = [-1]*len(WellVolumes)

	while(True): 
		Height += HEIGHT_INCREMENT
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
		CalcHeight = 0
		EquationString = segment["SegmentEquation"]

		if Height >= segment["MaxSegmentHeight"]:
			CalcHeight = segment["MaxSegmentHeight"]
		else:
			CalcHeight = Height

		EquationString = EquationString.replace("x",str(CalcHeight))
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
	try:
		return DeckLoading[LabwareName]
	except:
		return None

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
	StepPreferredLoading[Item] = LoadingArray

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

	DeadVolumeConfig = SysConfig["Dead Volume"]

	Loading = {}

	PlateSequences = {k: v for k, v in Sequences.items() if "Plate" == v["Labware Category"]}

	for Plate in Plates_List:
		PlateType = Plate.GetType()
		MaxVol = Plate.GetVolume()
		LidRequired = Plate.GetLidState()

		Possibles = collections.OrderedDict({k: v for k, v in PlateSequences.items() if v["Max Supported Volume"] >= (MaxVol + DeadVolumeConfig[v["Labware Name"]]) and PlateType == v["Labware Type"] and int(not not v["Lid Sequence"]) >= int(not not LidRequired)})
		Possibles = collections.OrderedDict({k: v for k, v in sorted(Possibles.items(), key=lambda item: item[1]["Max Supported Volume"])})

		for item in Possibles:
			Possibles[item]["Used Volume"] = MaxVol + DeadVolumeConfig[Possibles[item]["Labware Name"]]

		Loading[Plate.GetName()] = {"PreferredCategories":[Plate.GetName(),Plate.GetType()], "Sequences":collections.OrderedDict(copy.deepcopy(Possibles))}

	ReagentSequences = {k: v for k, v in Sequences.items() if "Reagent" == v["Labware Category"]}

	for Solution in Solutions_List:
		SolutionStorage = Solution.GetStorage()
		MaxVol = Solution.GetVolume()

		Possibles = {k: v for k, v in ReagentSequences.items() if v["Max Supported Volume"] >= (MaxVol + DeadVolumeConfig[v["Labware Name"]]) and SolutionStorage == v["Storage Condition"]}
		Possibles = collections.OrderedDict({k: v for k, v in sorted(Possibles.items(), key=lambda item: item[1]["Max Supported Volume"])})

		for item in Possibles:
			Possibles[item]["Used Volume"] = MaxVol + DeadVolumeConfig[Possibles[item]["Labware Name"]]

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

	global CheckSequences

	for item in FinalLoading:

		AddCheckSequence(FinalLoading[item]["Sequence"])
		if FinalLoading[item]["Labware Category"] == "Plates" and (not not FinalLoading[item]["Lid"]) != False:
			AddCheckSequence(FinalLoading[item]["Lid"])

	return FinalLoading

def NumericToAlphaNumeric(Number):
	Alpha = int((Number-1) / 8)
	Numeric = Number % 8
	if Numeric == 0:
		Numeric = 8
	AN = str(chr(65+Alpha)) + str(Numeric)
	return AN


def GeneratePrepSheet(LabwareArray):
	global SysConfig

	StartRow = 2
	StartCol = 2
	MaxCol = 11
	CurrentRow = StartRow
	CurrentCol = StartCol
	RowPadding = 2
	ColPadding = 2
	RowTracker = 0

	try:
		EXCELIO.DeleteSheet("PrepList")
	except:
		pass

	EXCELIO.CreateSheet("PrepList")

	for Labware in LabwareArray:
		IsPlate = PLATES.IsPlate(Labware)

		if IsPlate == True and PLATES.GetPlate(Labware).LoadingRequired():
			Plate = PLATES.GetPlate(Labware)
			LoadingDict = GetDeckLoading(Labware)

			if LoadingDict != None:
				DeadVolumeConfig = SysConfig["Dead Volume"]

				PlatePrepArray = []
				for index in range(0,SAMPLES.GetNumSamples()):
					for position in Plate.GetSequenceList()[index]:
						if Plate.GetVolumesList()[index] != 0:
							PlatePrepArray.append({"Position":position,"AlphaNumeric":NumericToAlphaNumeric(position),"Volume":abs(Plate.GetVolumesList()[index]) + DeadVolumeConfig[LoadingDict["Labware Name"]]})

				PlatePrepArray = sorted(PlatePrepArray, key=lambda x: x["Position"])
				
				UsedSpace = EXCELIO.PrintPlate(CurrentRow, CurrentCol, Plate.GetName(), LoadingDict["Labware Name"], 8, 12, PlatePrepArray)

				NewRow = UsedSpace[0] + CurrentRow
				NewCol = UsedSpace[1] + CurrentCol
				
				if NewRow > RowTracker:
					RowTracker = NewRow

				if NewCol > MaxCol:
					CurrentCol = StartCol
					CurrentRow = RowTracker + RowPadding
				else:
					CurrentCol = NewCol + ColPadding
			#Do plate solution sheet here


	CurrentRow = RowTracker + RowPadding * 2
	CurrentCol = StartCol

	for Labware in LabwareArray:
		IsPlate = PLATES.IsPlate(Labware)
		if IsPlate == False:
			LoadingDict = GetDeckLoading(Labware)

			if LoadingDict != None:

				UsedSpace = EXCELIO.PrintReagent(CurrentRow, CurrentCol, Labware, LoadingDict["Labware Name"], LoadingDict["Volume"])

				NewRow = UsedSpace[0] + CurrentRow
				NewCol = UsedSpace[1] + CurrentCol
				
				if NewRow > RowTracker:
					RowTracker = NewRow

				if NewCol > MaxCol:
					CurrentCol = StartCol
					CurrentRow = RowTracker + RowPadding
				else:
					CurrentCol = NewCol + ColPadding
			#Do reagent solution loading here

	EXCELIO.AutoFit("PrepList")	





