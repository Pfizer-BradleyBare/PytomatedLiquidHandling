

TITLE = 0
ROW = 1
COL = 2
PARENT_PLATE_NAME = 3
PARENT_PLATE_CATEGORY = 4
PARAMS_START = 4
#array Indices

NOT_EXCEL_COORDINATES = (0,0)

HAMILTON_STORAGE_COLD = "Cold"
HAMILTON_STORAGE_RT = "RT"
#Hamilton function specific constants

import copy
from ...General import ExcelIO as EXCELIO
from ..Steps import Plate as PLATE
from ..Steps import Split_Plate as SPLIT_PLATE

Unfiltered_Steps_List = []
Steps_List = []
Temp_Steps_List = []
Current_Step = []
StartingPlateName = ""


def GetAllSteps():
	global Unfiltered_Steps_List
	return Unfiltered_Steps_List


def StartStepSequence():
	global Steps_List
	global Temp_Steps_List

	Temp_Steps_List = copy.deepcopy(Steps_List)

def GetNextStep(ActivePlates):
	global Temp_Steps_List
	global Current_Step

	for step in Temp_Steps_List:
		Plate = step.GetParentPlate()

		if Plate in ActivePlates:
			Current_Step = copy.deepcopy(step)
			Temp_Steps_List.remove(step)
			return copy.deepcopy(step)

	return None

def UpdateStepParams(Step):
	Method = EXCELIO.GetMethod()

	Coords = Step.GetCoordinates()
	Row = Coords[0]
	Col = Coords[1]

	while True:
		Row += 1
		if Method[Row][Col] == None:
			break
		Step.AddParameters(Method[Row][Col],Method[Row][Col+1])


def GetCurrentStep():
	global Current_Step
	return Current_Step

def GetSteps():
	global Steps_List
	return Steps_List

def GetStartingPlate():
	global StartingPlateName
	return StartingPlateName

class Class:
	def __str__(self):
		print("Step Title:", self.Title)
		print("Step Coordinates: (",self.Row,",",self.Col,")")
		print("Parent Plate:", self.GetParentPlate())
		return "Step Parameters: " + str(self.Parameters)

	def __init__(self, Title):
		self.Title = Title
		
		self.Row = None
		self.Col = None

		self.Parent = None

		self.Parameters = {}

	def __eq__(self,other):
		if not isinstance(other, Class):
			return False
		return self.Title == other.Title and self.Row == other.Row and self.Col == other.Col and self.Parent == other.Parent and self.Parameters == other.Parameters

	def GetTitle(self):
		return self.Title

	def SetCoordinates(self,Row,Col):
		self.Row = Row
		self.Col = Col
	def GetCoordinates(self):
		return (self.Row,self.Col)

	def SetParentPlateStep(self, Parent):
		self.Parent = Parent
	
	def GetParentPlateStep(self):
		return self.Parent

	def GetParentPlate(self):
			return self.GetParentPlateStep().GetParameters()[PLATE.NAME]

	def AddParameters(self, Key, Value):
		self.Parameters[Key] = Value
		
	def GetParameters(self):
		return self.Parameters

def Init(PulledMethodSheet):
		global Steps_List
		global Unfiltered_Steps_List
		global StartingPlateName
		Steps_List = []

		Col_List = []

		for col in range(0,EXCELIO.METHOD_COL_END - EXCELIO.METHOD_COL_START + 1):
			
			Name = Class(PLATE.TITLE)
			Name.SetCoordinates(None,None)
			Name.SetParentPlateStep(None)
			Name.AddParameters(PLATE.NAME,None)
			Name.AddParameters(PLATE.TYPE,None)	
			Row_List = []
			
			for row in range(0,EXCELIO.METHOD_ROW_END - EXCELIO.METHOD_ROW_START + 1):
				
				value = PulledMethodSheet[row][col]
				
				if value != None and type(value) == str and value.lower() == "Comments".lower():
				
					Step = Class(PulledMethodSheet[row][col - 2])
					Step.SetCoordinates(EXCELIO.METHOD_ROW_START + row - 1, EXCELIO.METHOD_COL_START + col - 2 - 1)
					Step.SetParentPlateStep(Name)	

					if Step.GetTitle() == PLATE.TITLE:
						Name = Step

					pr = 1
					while(True):
						Key = PulledMethodSheet[row + pr][col - 2]
						Value = PulledMethodSheet[row + pr][col - 1]
						if(Key == None):
							break
						Step.AddParameters(Key,Value)
						pr += 1
					Row_List.append(Step)
			if len(Row_List) != 0:
				Col_List.append(Row_List)
		#organize steps by columns

		for Col in copy.deepcopy(Col_List):
			for Step in Col:
				if Step.GetTitle() == SPLIT_PLATE.TITLE:
					Col_List.append(Col[:Col.index(Step)+1])
					Col_List.append(Col[Col.index(Step)+1:])
					Col_List.remove(Col)
		#split columns that contain a split plates function

		for Col in Col_List:
			if len(Col) == 0:
				Col_List.remove(Col)
		#remove empty lists

		for Col in Col_List:
			if Col[0].GetTitle() != PLATE.TITLE:
				Col_List.remove(Col)
		#remove columns that do not start with a plate

		Col_List = sorted(Col_List, key=lambda x: x[0].GetCoordinates()[0])
		#Sort in descending order

		Row = Col_List[0][0].GetCoordinates()[0]
		#Get first row that steps begin

		Pathways = []
		Pathways.append(Col_List[0])
		Col_List.pop(0)
		#Get our starting pathway and remove path from list

		def __GetPathway(PlateName):
			for index in range(0,len(Col_List)):
				if Col_List[index][0].GetParameters()[PLATE.NAME] == PlateName:
					return Col_List.pop(index)

		while len(Pathways) != 0:

			Add_List = []
			Remove_List = []

			for Path in Pathways:
				
				try:
					Step = Path.pop(0)
					while "DISABLED".lower() in Step.GetTitle().lower():
						Step = Path.pop(0)
				except:
					Remove_List.append(Path)
					Step = None

				if Step != None:

					Steps_List.append(Step)

					if Step.GetTitle() == SPLIT_PLATE.TITLE:
						Remove_List.append(Path)
						Pathway1 = __GetPathway(Step.GetParameters()[SPLIT_PLATE.NAME_1])
						Pathway1[0].SetParentPlateStep(Step.GetParentPlateStep())

						Pathway2 = __GetPathway(Step.GetParameters()[SPLIT_PLATE.NAME_2])
						Pathway2[0].SetParentPlateStep(Step.GetParentPlateStep())
						
						Add_List.append(Pathway1)
						Add_List.append(Pathway2)

			for item in Remove_List:
				Pathways.remove(item)

			for item in Add_List:
				Pathways.append(item)

		Unfiltered_Steps_List = copy.deepcopy(Steps_List)
		#Save all steps for future use

		StartingPlateName = Steps_List[0].GetParameters()[PLATE.NAME]







#end
#End