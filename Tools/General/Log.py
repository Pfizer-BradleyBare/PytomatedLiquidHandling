from ..General import ExcelIO as EXCELIO
from ..General import HamiltonIO as HAMILTONIO
from ..User import Samples as SAMPLES
import math

PRERUN_SHEET = "TestLog"
TRUERUN_SHEET = "RunLog"

STEP_IDENTIFIER = "Step Title:"
LATEST_STEP_INFO = {}

LOG_ROW_START = 2
LOG_COL_START = 2
LOG_ROW_END = 1000
LOG_COL_END = 200 + LOG_COL_START

LOG_COL_STEP = 0
LOG_COL_COMMENTS = 1
LOG_COL_COMMAND = 2
LOG_COL_HAMILTON = 3

LOG_ROW_PADDING = 1
LOG_NEXT_LINE_PADDING = 4

TrueRunRow = LOG_ROW_START
CurrentRow = LOG_ROW_START
LogSheet = None


LogExists = True

GeneralCommentCounter = 0
StepCoordinates = None

def GetCommandID():
	global StepCoordinates
	return "("+str(StepCoordinates[0])+","+str(StepCoordinates[1])+")"

def Exists():
	global LogExists
	return LogExists

def GetLatestStep():
	global LATEST_STEP_INFO
	return LATEST_STEP_INFO

def StartStepLog(StepCoords):
	global StepCoordinates
	StepCoordinates = StepCoords

def EndStepLog():
	global CurrentRow
	global LOG_NEXT_LINE_PADDING
	global GeneralCommentCounter
	CurrentRow += LOG_NEXT_LINE_PADDING
	GeneralCommentCounter = 0
######################################################################### 
#	Description: Initializes the library by pulling information from Config files
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Init():
	global PRERUN_SHEET
	global TRUERUN_SHEET
	global LogSheet
	global TrueRunRow
	global CurrentRow
	global LogExists
	global STEP_IDENTIFIER
	global LATEST_STEP_INFO

	try:
		EXCELIO.Pull(TRUERUN_SHEET,1,1,1,1)
	except:
		LogExists = False

	if HAMILTONIO.IsSimulated() == True:
		LogSheet = PRERUN_SHEET
		try:
			EXCELIO.DeleteSheet(LogSheet)
			pass
		except:
			pass
		EXCELIO.CreateSheet(LogSheet)
	else:
		LogSheet = TRUERUN_SHEET
		try:
			LogExists = True
			EXCELIO.Pull(TRUERUN_SHEET,1,1,1,1)
		except:
			LogExists = False
			EXCELIO.CreateSheet(LogSheet)
	#This is a mess... I got nothing here

	if LogExists == True:
		Log = EXCELIO.Pull(TRUERUN_SHEET, LOG_ROW_START, LOG_COL_START, LOG_ROW_END, LOG_COL_END, n=2)
		for RowIndex in range(0,len(Log)):
			for Col in Log[RowIndex]:
				if Col != None:
					TrueRunRow = RowIndex + LOG_ROW_START
		#If the sheet exists then we need to find the end of the sheet so we can continue to append log information

		for RowIndex in range(TrueRunRow - LOG_ROW_START, 0, -1):
			if Log[RowIndex][LOG_COL_STEP] != None and STEP_IDENTIFIER in Log[RowIndex][LOG_COL_STEP]:
				LATEST_STEP_INFO["Title"] = Log[RowIndex][LOG_COL_STEP]
				LATEST_STEP_INFO["Coordinates"] = Log[RowIndex+1][LOG_COL_STEP]
				break
		#We know the end of the sheet. So lets work backward until we find the last step run.
	if HAMILTONIO.IsSimulated() == False:
		CurrentRow = TrueRunRow



def CommandInLog(Command):
	global LogSheet

	SearchArray = []

	while True:
		CommandLineEnd = Command.find("[",1)
		SearchArray.append(Command[:CommandLineEnd].replace("\n","").replace("]","]"+HAMILTONIO.GetDelimiter()).split(HAMILTONIO.GetDelimiter()))
		if CommandLineEnd == -1:
			break
		Command = Command[CommandLineEnd:]
	
	MaxLength = max(len(Command) for Command in SearchArray)
	SearchArray = [Command + [""]*(MaxLength - len(Command)) for Command in SearchArray]
	#We have created our search array. Now let us find the command

	Log = EXCELIO.Pull(LogSheet, LOG_ROW_START, LOG_COL_START, LOG_ROW_END, LOG_COL_END, n=2)

	for RowIndex in range(0,LOG_ROW_END-LOG_ROW_START):
		
		Status = True

		if Log[RowIndex][LOG_COL_COMMAND] != None and str(Log[RowIndex][LOG_COL_COMMAND]) == str(SearchArray[0][0]):

			for SRowIndex in range(0,len(SearchArray)):
				for SColIndex in range(0,len(SearchArray[SRowIndex])):
					try:
						LogValue = str(float(Log[RowIndex + SRowIndex][LOG_COL_COMMAND + SColIndex]))
					except:
						LogValue = str(Log[RowIndex + SRowIndex][LOG_COL_COMMAND + SColIndex])
						if LogValue == "None":
							LogValue = ""
					try:
						SearchValue = str(float(SearchArray[SRowIndex][SColIndex]))
					except:
						SearchValue = str(SearchArray[SRowIndex][SColIndex])
					#I need to do some silly casting because of the way excell works. Basically, if it is a number then we get the decimal and convert to string. 
					#Else we go directly to string

					if LogValue != SearchValue:
						Status = False
			if Status == True:
				print(True)
				return True
	print(SearchArray)
	print(False)
	return False




def HandleResponse(Response):
	RUN_BEGINNING = "Run From Beginning of Method"
	RUN_STEP = "Run From Above Step"
	RUN_BEFORE_STEP = "Run Step Before Above Step"
	RUN_AFTER_STEP = "Run Step After Above Step"

	print(Response)

	global TRUERUN_SHEET
	global TrueRunRow

	StepsToRemove = 0

	Log = EXCELIO.Pull(TRUERUN_SHEET, LOG_ROW_START, LOG_COL_START, LOG_ROW_END, LOG_COL_END, n=2)
	EXCELIO.DeleteSheet(TRUERUN_SHEET)
	EXCELIO.CreateSheet(TRUERUN_SHEET)

	if Response == RUN_BEGINNING:
		return

	elif Response == RUN_STEP:
		StepsToRemove = 1

	elif Response == RUN_BEFORE_STEP:
		StepsToRemove = 2

	elif Response == RUN_AFTER_STEP:
		pass
	else:
		print("No response matches found. Quitting...")
		quit()

	for RowIndex in range(TrueRunRow - LOG_ROW_START, 0, -1):
		if StepsToRemove == 0:
			TrueRunRow = RowIndex
			break
		if Log[RowIndex][LOG_COL_STEP] != None and STEP_IDENTIFIER in Log[RowIndex][LOG_COL_STEP]:
			StepsToRemove -= 1

	EXCELIO.Push(TRUERUN_SHEET, LOG_ROW_START, LOG_COL_START, LOG_ROW_START, LOG_COL_START, Log[:TrueRunRow])




def GeneralComment(Comment):
	global CurrentRow
	global GeneralCommentCounter
	GeneralCommentCounter += 1
	EXCELIO.Push(LogSheet, CurrentRow, LOG_COL_COMMENTS + LOG_COL_START, CurrentRow, LOG_COL_COMMENTS + LOG_COL_START, [[Comment]])
	CurrentRow += 1

def Step(Step):
	global LogSheet
	global CurrentRow
	global LOG_ROW_PADDING
	global GeneralComments

	printArray = []

	printArray.append(["Step Title: " + Step.GetTitle()])
	Coords = Step.GetCoordinates()
	printArray.append(["Excel Location (Row,Col): (" + str(Coords[0]) + "," + str(Coords[1]) + ")"])

	StepParams = Step.GetParameters()
	for Param in StepParams:
		In = SAMPLES.InColumn(StepParams[Param])
		LogString = Param + ": " + str(StepParams[Param])
		if In == True:
			LogString += " (Worklist Column) "
		printArray.append([LogString])

	EXCELIO.Push(LogSheet, CurrentRow, LOG_COL_STEP + LOG_COL_START, CurrentRow, LOG_COL_STEP + LOG_COL_START, printArray)

	CurrentRow += len(printArray) + LOG_ROW_PADDING

def Command(Command):
	global LogSheet
	global CurrentRow
	global LOG_ROW_PADDING
	global GeneralCommentCounter

	if GeneralCommentCounter == 0:
		GeneralComment("Step Parameters are as expected.")
	GeneralCommentCounter = 0

	CurrentRow += LOG_ROW_PADDING

	printArray = []

	while True:
		CommandLineEnd = Command.find("[",1)
		printArray.append(Command[:CommandLineEnd].replace("\n","").replace("]","]"+HAMILTONIO.GetDelimiter()).split(HAMILTONIO.GetDelimiter()))
		if CommandLineEnd == -1:
			break
		Command = Command[CommandLineEnd:]
	
	MaxLength = max(len(Command) for Command in printArray)
	printArray = [Command + [""]*(MaxLength - len(Command)) for Command in printArray]

	EXCELIO.Push(LogSheet, CurrentRow, LOG_COL_COMMAND + LOG_COL_START, CurrentRow, LOG_COL_COMMAND + LOG_COL_START, printArray)

	CurrentRow += len(printArray) + LOG_ROW_PADDING

def Hamilton(IDKHowToDoThisLOL):
	pass






