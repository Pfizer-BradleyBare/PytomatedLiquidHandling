from ..General import ExcelIO as EXCELIO
from ..General import HamiltonIO as HAMILTONIO
from ..User import Samples as SAMPLES

LOG_ROW_START = 2
LOG_COL_START = 2
LOG_ROW_END = 50000
LOG_COL_END = 110

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
FlushRowRanges = []
LogNumStepComments = 0
LogNumStepLines = 0
#These are the new variables

def Init(LogSheetName, ResetSheet):
	global LogSheet
	global Log
	global LogNextEmptyIndex

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

	Log = Log[:LogNextEmptyIndex]
	Log = [Row + [None]*(5 - len(Row)) for Row in Log]


def WriteLog(StartRow, StartCol, Array2D):
	global LogNextEmptyIndex
	global Log

	LogNextEmptyIndex += len(Array2D)

	Array2D = [[None] * StartCol + Row for Row in Array2D]
	Array2D = [Row + [None]*(5 - len(Row)) for Row in Array2D]

	if StartRow >= len(Log):
		Log += Array2D
	else:
		Log = Log[:StartRow] + Array2D + Log[StartRow:]

	FlushRowRanges.append(StartRow)

def UpdateLog(StartRow, StartCol, Array2D):
	global Log

	UpdateLength = len(Array2D)

	Array2D = [[None] * StartCol + Row for Row in Array2D]
	Array2D = [Row + [None]*(5 - len(Row)) for Row in Array2D]

	if StartRow >= len(Log):
		Log += Array2D
	else:
		Log = Log[:StartRow] + Array2D + Log[StartRow + UpdateLength:]

	FlushRowRanges.append(StartRow)

def PublishLog():
	global FlushStartRow

	if len(FlushRowRanges) != 0:
		Row = min(FlushRowRanges)
		PrintRow = Log[Row:]

		MaxLength = max(len(Row) for Row in PrintRow)
		PrintRow = [Row + [""]*(MaxLength - len(Row)) for Row in PrintRow]

		EXCELIO.WriteSheet(LogSheet,LOG_ROW_START + Row, LOG_COL_START, PrintRow)

	FlushStartRow = []

def LogStep(Step):
	global LogNumStepComments
	global LogNumStepLines

	LogNumStepComments = 0

	printArray = [[None]] * LOG_NEXT_LINE_PADDING
	#Padding so the log is easier to look at

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

	LogNumStepLines = len(printArray) - LOG_NEXT_LINE_PADDING

	if LogFindStep(Step) == -1:
		WriteLog(LogNextEmptyIndex,LOG_COL_STEP,printArray)

def LogFindStep(Step):

	Coords = Step.GetCoordinates()
	SearchValue = "Excel Location (Row,Col): (" + str(Coords[0]) + "," + str(Coords[1]) + ")"

	for Row in range (0,LogNextEmptyIndex):
		if Log[Row][LOG_COL_STEP] == SearchValue:
			return Row
	return -1

def LogMethodComment(Step, CommentList):
	Coords = Step.GetCoordinates()

	Comments = [[Comment] for Comment in CommentList]

	EXCELIO.WriteSheet("Method",Coords[0],Coords[1] + 3,Comments)
	
	EXCELIO.CreateMessageBox("There were issues found with your method. Please go to the method sheet and correct the errors. Errors will be documented to the right of the block.","Critical Validation Error!")
	quit()
	

def LogComment(Step, Comment):
	global LogNumStepComments

	if LogFindStep(Step) != -1:
		StepRow = LogFindStep(Step) - 1 + LogNumStepLines + LogNumStepComments

		if LogNumStepComments == 0:
			try:
				if Log[StepRow][LOG_COL_COMMENTS] == None:
					pass
				else:
					WriteLog(StepRow,LOG_COL_COMMENTS,[[None]])
					pass

			except:
				WriteLog(StepRow,LOG_COL_COMMENTS,[[None]])
				pass
				#I have to do this try, except because the line may not yet exists. I know it sucks
			LogNumStepComments += 1
			StepRow += 1

		try:
			if Log[StepRow][LOG_COL_COMMENTS] == Comment:
				pass
			else:
				WriteLog(StepRow,LOG_COL_COMMENTS,[[Comment]])
				pass

		except:
			WriteLog(StepRow,LOG_COL_COMMENTS,[[Comment]])
			pass
		#I have to do this try, except because the line may not yet exists. I know it sucks
	
		LogNumStepComments += 1

def LogCommand(CommandString):
	global CommandLogCounter
	CommandLogCounter += 1

	if LogFindCommand(CommandLogCounter) == -1:

		printArray = [[None]] * LOG_ROW_PADDING
		#Padding so the log is easier to look at

		while True:
			CommandLineEnd = CommandString.find("[",1)
			if CommandLineEnd == -1:
				printArray.append(CommandString[:].replace("\n","").replace("]","]"+HAMILTONIO.GetDelimiter()).split(HAMILTONIO.GetDelimiter()))
				break
			else:
				printArray.append(CommandString[:CommandLineEnd].replace("\n","").replace("]","]"+HAMILTONIO.GetDelimiter()).split(HAMILTONIO.GetDelimiter()))
			CommandString = CommandString[CommandLineEnd:]
		
		printArray.append(["### " + str(CommandLogCounter) + " ###"])
		printArray.append(["### Not Yet Executed ###"])
		printArray.append([None])
		printArray.append([None])
		printArray.append([None])

		WriteLog(LogNextEmptyIndex,LOG_COL_COMMAND,printArray)

	return CommandLogCounter

def LogFindCommand(CommandID):
	for Row in range (0,LogNextEmptyIndex):
		if str(Log[Row][LOG_COL_COMMAND]) == "### " + str(CommandID) + " ###":
			return Row
	return -1

def LogCommandExecutedRepeatable(CommandID):
	Row = LogFindCommand(CommandID)
	UpdateLog(Row + 1,LOG_COL_COMMAND,[["### Executed (Special) ###"]])

def LogCommandExecuted(CommandID):
	Row = LogFindCommand(CommandID)
	UpdateLog(Row + 1,LOG_COL_COMMAND,[["### Executed ###"]])

def LogCommandInProgress(CommandID):
	Row = LogFindCommand(CommandID)
	UpdateLog(Row + 1,LOG_COL_COMMAND,[["### Execution In Progress ###"]])

def LogCommandIsExecuted(CommandID):
	Row = LogFindCommand(CommandID)

	if str(Log[Row + 1][LOG_COL_COMMAND]) == "### Executed ###":
		return True
	else:
		return False

def LogCommandResponse(CommandID, ResponseDict):
	Row = LogFindCommand(CommandID)
	ReturnID = ResponseDict["ReturnID"]
	ReturnMessage = ResponseDict["ReturnMessage"]
	try:
		Response = ResponseDict["Response"]
	except:
		Response = "N/A"

	UpdateLog(Row + 2,LOG_COL_COMMAND,[["Return ID",ReturnID],["Return Message",ReturnMessage],["Response"] + Response.split(HAMILTONIO.GetDelimiter())])

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






