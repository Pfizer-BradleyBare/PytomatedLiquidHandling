
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

def Init(ExcelFile):
	global Excel_File
	Excel_File = ExcelFile

def Pull(Sheet, RowStart, ColStart, RowEnd, ColEnd, n=1):
	global Excel_File
	if Excel_File == None:
		print("ExcelIO -- Init First")
		return None
	else: 
		return xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).options(ndim=n).value

def Push(Sheet, RowStart, ColStart, RowEnd, ColEnd, Data):
	global Excel_File
	if Excel_File == None:
		print("ExcelIO -- Init First")
		return False
	else: 
		xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).value = Data
		return True

def GetMethod():
	return Pull(METHOD_SHEET, METHOD_ROW_START, METHOD_COL_START, METHOD_ROW_END, METHOD_COL_END,2)

def GetWorklist():
	return Pull(WORKLIST_SHEET, WORKLIST_ROW_START, WORKLIST_COL_START, WORKLIST_ROW_END, WORKLIST_COL_END,2)
