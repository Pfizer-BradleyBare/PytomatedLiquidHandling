from ..General import ExcelIO as EXCELIO
from ..General import HamiltonIO as HAMILTONIO
from ..User import Samples as SAMPLES
import math

LOG_ROW_START = 2
LOG_COL_START = 2
LOG_ROW_END = 25000
LOG_COL_END = 105

LOG_COL_STEP = 0
LOG_COL_COMMENTS = 1
LOG_COL_COMMAND = 2
LOG_COL_HAMILTON = 3

LOG_ROW_PADDING = 1
LOG_NEXT_LINE_PADDING = 4

LogSheet = None
Log = None
LogNextEmptyIndex = 0
CommandLogCounter = 0
#These are the new variables

def Init(LogSheetName, ResetSheet):
	global LogSheet
	global Log
	global CommandLogCounter
	global LogNextEmptyIndex

	CommandLogCounter = 0
	LogNextEmptyIndex = 0
	LogSheet = LogSheetName

	if ResetSheet == True:
		EXCELIO.DeleteSheet(LogSheet)
	EXCELIO.CreateSheet(LogSheet)

	Log = EXCELIO.Pull(LogSheet, LOG_ROW_START, LOG_COL_START, LOG_ROW_END, LOG_COL_END, n=2)
	#The first thing we want to do is pull the log. Now when we execute steps we can look for the existance of that step
	
	while True:
		
		LogSlice = Log[LogNextEmptyIndex:LogNextEmptyIndex+10]
		if all(Cell is None for Row in LogSlice for Cell in Row) == True:
			break

		LogNextEmptyIndex += 1
	#This will take a slice of 10 rows from the log, if all values are "None" then we can be confident we found the end of the log.

	Log = Log [:LogNextEmptyIndex]

FlushRowRanges = []
FlushColRanges = []
def UpdateLog(StartRow, StartCol, Array2D):
	global LogNextEmptyIndex

	WriteRow = StartRow
	WriteCol = StartCol

	FlushRowRanges.append(WriteRow)
	FlushColRanges.append(WriteCol)

	for Row in Array2D:
		WriteCol = StartCol
		for Item in Row:
			Log[WriteRow][WriteCol] = Item
			WriteCol += 1
		WriteRow += 1
	
	FlushRowRanges.append(WriteRow)
	FlushColRanges.append(WriteCol)

	LogNextEmptyIndex += WriteRow - StartRow

def PublishLog():
	global FlushColRanges
	global FlushRowRanges

	MinRow = min(FlushRowRanges)
	MaxRow = max(FlushRowRanges)
	MinCol = min(FlushColRanges)
	MaxCol = max(FlushColRanges)
	#We do not want to flush every line to the excel file. Only the areas that were updated. So lets find the min and max row and col

	FlushRowRanges = []
	FlushColRanges = []

	FlushArray = [Log[i][MinCol:MaxCol] for i in range(MinRow,MaxRow)]

	EXCELIO.WriteSheet(LogSheet,MinRow + LOG_ROW_START, MinCol + LOG_COL_START, FlushArray)


def LogStep(Step):
	global LogNextEmptyIndex

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

	LogNextEmptyIndex += LOG_NEXT_LINE_PADDING
	#Padding so the log is easier to look at

	UpdateLog(LogNextEmptyIndex,LOG_COL_STEP,printArray)

def LogFindStep(Step):
	Coords = Step.GetCoordinates()
	SearchValue = "Excel Location (Row,Col): (" + str(Coords[0]) + "," + str(Coords[1]) + ")"

	for Row in range (0,LogNextEmptyIndex):
		if Log[Row][LOG_COL_STEP] == SearchValue:
			return Row
	return -1

def LogIncrementCommandCounter():
	global CommandLogCounter
	CommandLogCounter += 1
	return CommandLogCounter

def LogCommand(CommandString):
	global LogNextEmptyIndex

	printArray = []

	while True:
		CommandLineEnd = CommandString.find("[",1)
		if CommandLineEnd == -1:
			printArray.append(CommandString[:].replace("\n","").replace("]","]"+HAMILTONIO.GetDelimiter()).split(HAMILTONIO.GetDelimiter()))
			break
		else:
			printArray.append(CommandString[:CommandLineEnd].replace("\n","").replace("]","]"+HAMILTONIO.GetDelimiter()).split(HAMILTONIO.GetDelimiter()))
		CommandString = CommandString[CommandLineEnd:]
	
	printArray.append(["##ID - " + str(CommandLogCounter)])

	MaxLength = max(len(Command) for Command in printArray)
	printArray = [Command + [""]*(MaxLength - len(Command)) for Command in printArray]

	LogNextEmptyIndex += LOG_ROW_PADDING
	#Padding so the log is easier to look at

	UpdateLog(LogNextEmptyIndex,LOG_COL_COMMAND,printArray)

def LogFindCommand(CommandID):

	for Row in range (0,LogNextEmptyIndex):
		if str(Log[Row][LOG_COL_COMMAND]) == str(CommandID):
			return Row
	return -1

def HandleResponse(Response):
	RUN_BEGINNING = "Run From Beginning of Method"
	RUN_STEP = "Run From Above Step"
	RUN_BEFORE_STEP = "Run Step Before Above Step"
	RUN_AFTER_STEP = "Run Step After Above Step"

	Response = Response["Log Selection"]

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
		EXCELIO.Push(TRUERUN_SHEET, LOG_ROW_START, LOG_COL_START, LOG_ROW_START, LOG_COL_START, Log)
		quit()

	for RowIndex in range(TrueRunRow - LOG_ROW_START, 0, -1):
		if StepsToRemove == 0:
			TrueRunRow = RowIndex
			break
		if Log[RowIndex][LOG_COL_STEP] != None and STEP_IDENTIFIER in Log[RowIndex][LOG_COL_STEP]:
			StepsToRemove -= 1

	EXCELIO.Push(TRUERUN_SHEET, LOG_ROW_START, LOG_COL_START, LOG_ROW_START, LOG_COL_START, Log[:TrueRunRow])






