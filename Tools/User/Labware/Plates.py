

from ..Steps import Plate as PLATE
from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
import copy

#this dict is in the format: PlateName: [Category, LidUsed, ActiveState, SequencesList, FactorsList, TotalVolumesList]. Then list are the length of the number of samples
Plates_List = {}

class Class:
	def __init__ (self,PlateName, Type, SequencesList):
		self.PlateName = PlateName
		self.Type = Type
		self.Lid = False
		self.ActiveState = False
		self.SequencesList = SequencesList
		self.FactorsList = [1] * len(SequencesList)
		self.VolumesList = [0] * len(SequencesList)

	def GetName(self):
		return self.PlateName

	def GetType(self):
		return self.Type

	def SetLidState(self):
		self.Lid = True

	def GetLidState(self):
		return self.Lid

	def GetSequenceList(self):
		return self.SequencesList

	def GetVolumesList(self):
		return self.VolumesList

	def GetVolume(self):
		MaxVol = 0
		for vol in self.GetVolumesList():
			if vol > MaxVol:
				MaxVol = vol
		return MaxVol

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

	def CreatePipetteSequence(self, SourceList, SourceVolumeList):
		global Plates_List

		Expanded = []

		for count in range(0,len(self.GetSequenceList())):

			ActualVolume = SourceVolumeList[count] * self.GetFactors()[count]
			
			for Position in self.GetSequenceList()[count]:
			
				Expanded.append([int(float(Position)), SourceList[count], ActualVolume, self.GetVolumesList()[count]])
			
			self.GetVolumesList()[count] += ActualVolume

		return copy.deepcopy(sorted(Expanded, key=lambda x: x[0]))

#This function adds a plate object to the dictionary. Category is the plate type and Sequences list is the 
def AddPlate(PlateName, Type, SequencesList):
	global Plates_List
	Plates_List[PlateName] = Class(PlateName, Type, SequencesList)

def GetPlate(PlateName):
	global Plates_List
	if PlateName in Plates_List:
		return Plates_List[PlateName]
	else:
		return None

def GetActivePlates():
	global Plates_List

	ActiveList = []

	for plate in Plates_List:
		if Plates_List[plate].IsActive():
			ActiveList.append(plate)

	return ActiveList

def Init():
	global Plates_List
	Plates_List = {}

def IsPlate(PlateName):
	global Plates_List
	if PlateName in Plates_List:
		return True
	return False

#A dead plate is a plate that is not used in this method sequence. Dead plates orginate from the Split plate step
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

#This function will return all plate objects that are not dead
def GetPlates():
	Temp = []
	DeadPlates = GetDeadPlates()

	global Plates_List

	for Plate in Plates_List:
		plate = Plates_List[Plate]

		if Plate not in DeadPlates:
			MaxVol = 0

			for Vol in plate.GetVolumesList():
				if Vol > MaxVol:
					MaxVol = Vol
			Temp.append(plate)
	return Temp

def StartStepSequence(StartingPlateName):
	for key in Plates_List:
		if key == StartingPlateName:
			Plates_List[key].Activate()
		else:
			Plates_List[key].Deactivate()



