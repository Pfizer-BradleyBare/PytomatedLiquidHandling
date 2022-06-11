import copy
from ...General import ExcelIO as EXCELIO
from ..Steps import Plate as PLATE
from ..Steps import Split_Plate as SPLIT_PLATE

ActiveContextTracker = set()
def ActivateContext(Context):
	ActiveContextTracker.add(Context)
def DeactivateContext(Context):
	ActiveContextTracker.remove(Context)
def GetNumActiveContexts():
	return len(ActiveContextTracker)

FrozenContextTracker = set()
def FreezeContext(Context):
	FrozenContextTracker.add(Context)
def ThawContext(Context):
	FrozenContextTracker.remove(Context)

Unfiltered_Steps_List = []
Steps_List = []
Temp_Steps_List = []
Current_Step = None
NumExecutedSteps = 0

def GetTotalNumSteps():
	return len(Steps_List)

def GetNumExecutedSteps():
	return NumExecutedSteps

def StartStepSequence():
	global Steps_List
	global Temp_Steps_List

	Temp_Steps_List = copy.deepcopy(Steps_List)
	ActivateContext(Temp_Steps_List[0].GetContext())

def GetNextStep():
	global Temp_Steps_List
	global Current_Step
	global ActiveContextTracker

	for step in Temp_Steps_List:
		Context = step.GetContext()

		if Context in ActiveContextTracker and not (Context in FrozenContextTracker):
			Current_Step = copy.deepcopy(step)
			Temp_Steps_List.remove(step)
			return copy.deepcopy(step)

	return None

def UpdateStepParams(Step):
	Method = EXCELIO.GetMethod()

	Coords = Step.GetCoordinates()
	Row = Coords[0] - 1
	Col = Coords[1] - 1

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

def GetStepIndex(Step):
	Steps = GetSteps()

	for index in range(0,len(Steps)):
		if Step == Steps[index]:
			return index

def GetPreviousStepInPathway(Step):
	Steps = GetSteps()
	Index = GetStepIndex(Step)

	StepContext = Step.GetContext()
	FoundStep = None
	for index in range(0,len(Steps)):
		if index == Index:
			break
		if Steps[index].GetContext() in StepContext:
			FoundStep = Steps[index]
	return FoundStep

def GetNextStepInPathway(Step):
	Steps = GetSteps()
	Index = GetStepIndex(Step)

	StepContext = Step.GetContext()
	FoundStep = None
	Done = False
	for index in range(0,len(Steps)):
		if Steps[index].GetContext() in StepContext:
			FoundStep = Steps[index]
			if Done == True:
				break
			if index == Index:
				Done = True
	return FoundStep

class Class:
	def __str__(self):
		print("Step Title:", self.Title)
		print("Step Coordinates: (",self.Row,",",self.Col,")")
		print("Parent Plate:", self.GetParentPlateName())
		print("Context:",self.Context)
		return "Step Parameters: " + str(self.Parameters)

	def __init__(self, Title):
		self.Title = Title
		
		self.Row = None
		self.Col = None

		self.Context = None

		self.Parameters = {}

	def __eq__(self,other):
		if not isinstance(other, Class):
			return False
		return self.Row == other.Row and self.Col == other.Col
		#Row and Col in excel file is always unique so we can find step using only those parameters.

	def GetTitle(self):
		return self.Title

	def SetCoordinates(self,Row,Col):
		self.Row = Row
		self.Col = Col
		
	def GetCoordinates(self):
		return (self.Row,self.Col)

	def GetParentPlateName(self):
		return self.Context[self.Context.rfind(":")+1:]
	
	def SetContext(self,Context):
		self.Context = Context
	
	def GetContext(self):
		return self.Context

	def GetParentContext(self):
		return self.Context[:self.Context.rfind(":")]

	def AddParameters(self, Key, Value):
		self.Parameters[Key] = Value
		
	def GetParameters(self):
		return self.Parameters

def Init(PulledMethodSheet):
		global Steps_List
		global Unfiltered_Steps_List
		Steps_List = []

		Col_List = []

		for col in range(0,EXCELIO.METHOD_COL_END - EXCELIO.METHOD_COL_START + 1):
			
			Name = Class(PLATE.TITLE)
			Name.SetCoordinates(None,None)
			Name.AddParameters(PLATE.NAME,None)
			Name.AddParameters(PLATE.TYPE,None)	
			Row_List = []
			
			for row in range(0,EXCELIO.METHOD_ROW_END - EXCELIO.METHOD_ROW_START + 1):
				
				value = PulledMethodSheet[row][col]
				
				if value != None and type(value) == str and value.lower() == "Comments".lower():
				
					Step = Class(PulledMethodSheet[row][col - 2].replace(" - (Click Here to Update)",""))
					Step.SetCoordinates(EXCELIO.METHOD_ROW_START + row, EXCELIO.METHOD_COL_START + col - 2)	

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

		for Col in Col_List:
			if Col[-1].GetTitle() != "Split Plate":
				if Col[-1].GetTitle() != "Finish":
					EXCELIO.CreateCriticalMessageBox("All pathways must be terminated by a Finish block. Please correct.","Method Unsatisfactory")
		#Checking that all pathways are terminated with Finish block.

		Pathways = []
		Pathways.append({"List":Col_List[0],"Context":""})
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
					Step = Path["List"].pop(0)
					while "DISABLED".lower() in Step.GetTitle().lower():
						Step = Path["List"].pop(0)
				except:
					Remove_List.append(Path)
					Step = None

				if Step != None:

					Steps_List.append(Step)
					Step.SetContext(Path["Context"])

					if Step.GetTitle() == PLATE.TITLE:
						Path["Context"] = Path["Context"] + ":" + str(Step.GetParameters()[PLATE.NAME])

					if Step.GetTitle() == SPLIT_PLATE.TITLE:
						Remove_List.append(Path)

						Pathway1 = __GetPathway(Step.GetParameters()[SPLIT_PLATE.NAME_1])
						Pathway2 = __GetPathway(Step.GetParameters()[SPLIT_PLATE.NAME_2])
						
						Add_List.append({"List":Pathway1,"Context":Path["Context"]})
						Add_List.append({"List":Pathway2,"Context":Path["Context"]})

			for item in Remove_List:
				Pathways.remove(item)

			for item in Add_List:
				Pathways.append(item)

		Unfiltered_Steps_List = copy.deepcopy(Steps_List)
		#Save all steps for future use