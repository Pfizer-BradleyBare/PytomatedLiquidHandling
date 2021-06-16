
import xlwings as xl

METHOD_ROW_START = 1
METHOD_COL_START = 1
METHOD_ROW_END = 1000
METHOD_COL_END = 500
WORKLIST_ROW_START = 1
WORKLIST_COL_START = 1
WORKLIST_ROW_END = 100
WORKLIST_COL_END = 100
#constants

METHOD_SHEET = "Method"
WORKLIST_SHEET = "Worklist"

Excel_File = None

######################################################################### 
#	Description: Initializes the Excel interface by setting the excel file to be used throughout the entire script
#	Input Arguments: [ExcelFile: String:Complete path to the excel file]
#	Returns: N/A
#########################################################################
def Init(ExcelFile):
	global Excel_File
	Excel_File = ExcelFile

######################################################################### 
#	Description: Reads a sheet from the excel file within specified range
#	Input Arguments: [Sheet: String:SheetName] [RowStart: Integer:1-indexed] [ColStart: Integer:1-indexed] 
#	[RowEnd: Integer:1-indexed] [ColEnd: Integer:1-indexed] [n: Integer: return array dimensions]
#	Returns: If not initialized then returns None, Else returns sheet in array format
#########################################################################
def Pull(Sheet, RowStart, ColStart, RowEnd, ColEnd, n=1):
	global Excel_File
	if Excel_File == None:
		print("ExcelIO -- Init First")
		return None
	else: 
		return xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).options(ndim=n).value

######################################################################### 
#	Description: Writes data to a sheet within specified range. NOTE: Range must match size of input array
#	Input Arguments: [Sheet: String:SheetName] [RowStart: Integer:1-indexed] [ColStart: Integer:1-indexed] 
#	[RowEnd: Integer:1-indexed] [ColEnd: Integer:1-indexed] [Data: 2D-Array]
#	Returns: If not initialized then false, else True
#########################################################################
def Push(Sheet, RowStart, ColStart, RowEnd, ColEnd, Data):
	global Excel_File
	if Excel_File == None:
		print("ExcelIO -- Init First")
		return False
	else: 
		xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).value = Data
		return True

######################################################################### 
#	Description: Pulls the entire method sheet 
#	Input Arguments: N/A
#	Returns: 2D-Array
#########################################################################
def GetMethod():
	return Pull(METHOD_SHEET, METHOD_ROW_START, METHOD_COL_START, METHOD_ROW_END, METHOD_COL_END,2)

######################################################################### 
#	Description: Pulls the entire worklist sheet 
#	Input Arguments: N/A
#	Returns: 2D-Array
#########################################################################
def GetWorklist():
	return Pull(WORKLIST_SHEET, WORKLIST_ROW_START, WORKLIST_COL_START, WORKLIST_ROW_END, WORKLIST_COL_END,2)
