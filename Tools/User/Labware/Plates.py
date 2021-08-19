

from ..Steps import Plate as PLATE
from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
from ...User import Configuration as CONFIGURATION
import copy

#this dict is in the format: PlateName: [Category, LidUsed, ActiveState, SequencesList, FactorsList, TotalVolumesList]. Then list are the length of the number of samples
Plates_List = {}

class Class:
######################################################################### 
#	Description: Initializes class to default starting parameters
#	Input Arguments: [PlateName: String] [Type: String] [SequencesList: List]
#	Returns: N/A
#########################################################################
	def __init__ (self,PlateName, Type, SequencesList):
		self.PlateName = PlateName
		self.Type = Type
		self.Lid = False
		self.Vacuum = False
		self.ActiveState = False
		self.SequencesList = SequencesList
		self.FactorsList = [1] * len(SequencesList)
		self.VolumesList = [0] * len(SequencesList)
		self.MaxVolume = 0
		self.RequiresLoading = False

	def GetName(self):
		return self.PlateName

	def GetType(self):
		return self.Type

	def SetLidState(self):
		self.Lid = True

	def ResetLidState(self):
		self.Lid = False

	def GetLidState(self):
		return self.Lid

	def SetVacuumState(self):
		self.Vacuum = True

	def ResetVacuumState(self):
		self.Vacuum = False

	def GetVacuumState(self):
		return self.Vacuum

	def GetSequenceList(self):
		return self.SequencesList

	def UpdateSequenceList(self, NewSequencesList):
		self.SequencesList = NewSequencesList

	def GetVolumesList(self):
		return self.VolumesList

	def UpdateMaxVolume(self):
		Sequences = self.GetSequenceList()
		Volumes = self.GetVolumesList()

		TotalVolumes = {}

		for SequenceList in Sequences:
			for Sequence in SequenceList:
				TotalVolumes[str(Sequence)] = 0

				for SequenceListIndex in range(0,len(Sequences)):
						if Sequence in Sequences[SequenceListIndex]:
							TotalVolumes[str(Sequence)] += Volumes[SequenceListIndex] * len(Sequences[SequenceListIndex])
		
		for Key in TotalVolumes:
			Volume = TotalVolumes[Key]
			if Volume < 0:
				self.RequiresLoading = True
			Volume = abs(Volume)
			if Volume > self.MaxVolume:
				self.MaxVolume = Volume

	def LoadingRequired(self):
		return self.RequiresLoading

######################################################################### 
#	Description: Returns the max well volume on this plate
#	Input Arguments: N/A
#	Returns: [Float]
#########################################################################
	def GetVolume(self):
		return self.MaxVolume

	def Activate(self):
		self.ActiveState = True

	def Deactivate(self):
		self.ActiveState = False

	def IsActive(self):
		return self.ActiveState

	def GetFactors(self):
		return self.FactorsList

	def UpdateFactors(self, NewFactorsList):
		self.FactorsList = NewFactorsList

######################################################################### 
#	Description: Creates a sorted pipetting list to be used by the hamilton pipette command
#	Input Arguments: [SourceList: List] [SourceVolumeList: List]
#	Returns: [List of Lists]
#########################################################################
	def CreatePipetteSequence(self, SourceList, SourceVolumeList, MixList):
		global Plates_List
		
		VolumesList = self.GetVolumesList()
		DispenseHeights = CONFIGURATION.WellVolumeToDispenseHeight(self.GetName(),VolumesList)
		DestinationPosition = self.GetSequenceList()

		Expanded = []

		for count in range(0,len(DestinationPosition)):

			ActualVolume = SourceVolumeList[count] * self.GetFactors()[count]

			if ActualVolume > 0:
			
				for count2 in range(0,len(DestinationPosition[count])):
					SourcePosition = DestinationPosition[count][count2]

					if IsPlate(SourceList[count]) == True:
						Plate = GetPlate(SourceList[count])
						SourcePosition = Plate.GetSequenceList()[count][count2]
						Plate.GetVolumesList()[count] -= ActualVolume
						Plate.UpdateMaxVolume()
					#Do plate volume subtraction

					Expanded.append({"Destination Position":int(float(DestinationPosition[count][count2])),"Destination":self.GetName(), "Source Position":int(float(SourcePosition)), "Source":SourceList[count], "Volume":ActualVolume, "Height":DispenseHeights[count], "Total":VolumesList[count], "Mix":MixList[count]})
			
				self.GetVolumesList()[count] += ActualVolume
				self.UpdateMaxVolume()
		
		return copy.deepcopy(sorted(Expanded, key=lambda x: x["Destination Position"]))

def Init():
	global Plates_List
	Plates_List = {}

######################################################################### 
#	Description: Creates a new plate class and adds it to the plate dictionary
#	Input Arguments: [PlateName: String] [Type: String] [SequencesList: List]
#	Returns: N/A
#########################################################################
def AddPlate(PlateName, Type, SequencesList):
	global Plates_List
	Plates_List[PlateName] = Class(PlateName, Type, SequencesList)

######################################################################### 
#	Description: Returns the plate class with PlateName
#	Input Arguments: [PlateName: String]
#	Returns: Plate class
#########################################################################
def GetPlate(PlateName):
	global Plates_List
	if PlateName in Plates_List:
		return Plates_List[PlateName]
	else:
		return None

######################################################################### 
#	Description: Returns the plates that are alive or active
#	Input Arguments: N/A
#	Returns: [List of strings]
#########################################################################
def GetActivePlates():
	global Plates_List

	ActiveList = []

	for plate in Plates_List:
		if Plates_List[plate].IsActive():
			ActiveList.append(plate)

	return ActiveList

######################################################################### 
#	Description: Confirms the the string argument is a valid plate
#	Input Arguments: [PlateName: String]
#	Returns: [bool]
#########################################################################
def IsPlate(PlateName):
	global Plates_List
	if PlateName in Plates_List:
		return True
	return False

######################################################################### 
#	Description: Returns the dead plates. Meaning the plates that will never be used in this sequence. Any steps that reference this plate are also dead
#	Input Arguments: N/A
#	Returns: [List of Strings]
#########################################################################
def GetDeadPlates():
	global Plates_List
	Temp = []

	for key in Plates_List:
		count = 0
		for factor in Plates_List[key].GetFactors():
			count += factor 
		if count == 0:
			Temp.append(key)
	return Temp

######################################################################### 
#	Description: Returns all plates that are not dead. Plates can either be active or inactive.
#	Input Arguments: N/A
#	Returns: [List of strings]
#########################################################################
def GetPlates():
	Temp = []
	DeadPlates = GetDeadPlates()

	global Plates_List

	for Plate in Plates_List:
		plate = Plates_List[Plate]

		if Plate not in DeadPlates and plate.GetVolume() > 0:
			Temp.append(plate)
	return Temp

######################################################################### 
#	Description: Makes the starting plate in the step sequence active.
#	Input Arguments: [StartingPlateName: String]
#	Returns: N/A
#########################################################################
def StartStepSequence(StartingPlateName):
	for key in Plates_List:
		if key == StartingPlateName:
			Plates_List[key].Activate()
		else:
			Plates_List[key].Deactivate()



