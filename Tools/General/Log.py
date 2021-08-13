from ..General import ExcelIO as EXCELIO
from ..General import HamiltonIO as HAMILTONIO
from ..User import Samples as SAMPLES

PRERUN_SHEET = "TestLog"
TRUERUN_SHEET = "RunLog"

STEP_IDENTIFIER = "Step Title:"
LATEST_STEP_INFO = {}

LOG_ROW_START = 2
LOG_COL_START = 2
LOG_ROW_END = 1000
LOG_COL_END = 5

LOG_COL_STEP = 0
LOG_COL_COMMENTS = 1
LOG_COL_COMMAND = 2
LOG_COL_HAMILTON = 3

LOG_ROW_PADDING = 1
LOG_NEXT_LINE_PADDING = 4

TrueRunRow = 0
CurrentRow = LOG_ROW_START
LogSheet = None


LogExists = True

GeneralCommentsLog = []
StepLog = []
CommandLog = []
HamiltonLog = []
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
		except:
			pass
		EXCELIO.CreateSheet(LogSheet)
	else:
		LogSheet = TRUERUN_SHEET
		try:
			LogExists = False
			EXCELIO.Pull(TRUERUN_SHEET,1,1,1,1)
		except:
			LogExists = True
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

def Exists():
	global LogExists
	return LogExists

def CommandInLog(Command):
	global LogSheet

	Log = EXCELIO.Pull(LogSheet, LOG_ROW_START, LOG_COL_START, LOG_ROW_END, LOG_COL_END, n=2)

	Coords = Step.GetCoordinates()
	SearchString = "Excel Location (Row,Col): (" + str(Coords[0]) + "," + str(Coords[1]) + ")"

	for Row in Log:
		if Row[LOG_COL_COMMAND] != None and SearchString in Row[LOG_COL_COMMAND]:
			return True
	return False

def GetLatestStep():
	global LATEST_STEP_INFO
	return LATEST_STEP_INFO

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


def StartNextLine():
	global CurrentRow
	global LOG_NEXT_LINE_PADDING
	CurrentRow += LOG_NEXT_LINE_PADDING

def GeneralComment(Comment):
	global GeneralComments
	GeneralComments.append([Comment])

def Step(Step, Comments):
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

	printArray.append(["Comments: " + str(Comments)])

	EXCELIO.Push(LogSheet, CurrentRow, LOG_COL_STEP + LOG_COL_START, CurrentRow, LOG_COL_STEP + LOG_COL_START, printArray)

	CurrentRow += len(printArray) + LOG_ROW_PADDING

	if len(GeneralComments) == 0:
		GeneralComments.append(["Step parameters are as expected"])
	EXCELIO.Push(LogSheet, CurrentRow, LOG_COL_COMMENTS + LOG_COL_START, CurrentRow, LOG_COL_COMMENTS + LOG_COL_START, GeneralComments)
	CurrentRow += len(GeneralComments) + LOG_ROW_PADDING
	GeneralComments = []

def Command(Command):
	global LogSheet
	global CurrentRow
	global LOG_ROW_PADDING

	printArray = []

	while True:
		CommandLineEnd = Command.find("[",1)
		if CommandLineEnd == -1:
			break
		printArray.append([Command[:CommandLineEnd].replace("\n","")])
		Command = Command[CommandLineEnd:]
	printArray.append([Command])

	EXCELIO.Push(LogSheet, CurrentRow, LOG_COL_COMMAND + LOG_COL_START, CurrentRow, LOG_COL_COMMAND + LOG_COL_START, printArray)

	CurrentRow += len(printArray) + LOG_ROW_PADDING

def Hamilton(IDKHowToDoThisLOL):
	pass






