
import xlwings as xl

METHOD_ROW_START = 1
METHOD_COL_START = 1
METHOD_ROW_END = 1000
METHOD_COL_END = 100
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

def CreateSheet(Sheet):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_CreateSheet")
			Macro(Sheet,"Solutions")
			break
		except:
			pass

def DeleteSheet(Sheet):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_DeleteSheet")
			Macro(Sheet)
			break
		except:
			pass

def Pull(Sheet, RowStart, ColStart, RowEnd, ColEnd, n=1):
	return xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).options(ndim=n).value

def PullUsedRange(Sheet):
	return xl.Book(Excel_File).sheets[Sheet].used_range.value

	
#
# Reading a sheet is easy. For Excel 2010, if you try to write a sheet while a save is ongoing is crashes the xlwings app. By using a macro it never crashes
#
def WriteSheet(Sheet,Row,Col,Text2DArray):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_WriteSheet")
			Macro(Sheet,Row,Col,Text2DArray)
			break
		except:
			pass

def GetMethod():
	return Pull(METHOD_SHEET, METHOD_ROW_START, METHOD_COL_START, METHOD_ROW_END, METHOD_COL_END,2)

def GetWorklist():
	return Pull(WORKLIST_SHEET, WORKLIST_ROW_START, WORKLIST_COL_START, WORKLIST_ROW_END, WORKLIST_COL_END,2)

def GetMethodValidatedStatus():
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("Python_GetMethodValidatedStatus")
			Macro()
			return Pull("BuildingBlocks",1,1,1,1)[0]
		except:
			pass

def CreateCriticalMessageBox(Message, Title):
	Macro = xl.Book(Excel_File).macro("PYTHON_CreateCriticalMessageBox")
	Macro(Message, Title)

def CreateInformationMessageBox(Message, Title):
	Macro = xl.Book(Excel_File).macro("PYTHON_CreateInformationMessageBox")
	Macro(Message, Title)

def SelectCell(Sheet,Row,Col):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_SelectCell")
			Macro(Sheet,Row,Col)
			break
		except:
			pass

def CreateBorder(Sheet,RowStart,ColStart,RowEnd,ColEnd,BorderStyle,BorderWeight):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_CreateBorder")
			Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd)
			break
		except:
			pass

def Merge(Sheet,RowStart,ColStart,RowEnd,ColEnd):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_Merge")
			Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd)
			break
		except:
			pass

def FontSize(Sheet,RowStart,ColStart,RowEnd,ColEnd, FontSize):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_FontSize")
			Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd, FontSize)
			break
		except:
			pass

def Center(Sheet,RowStart,ColStart,RowEnd,ColEnd):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_Center")
			Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd)
			break
		except:
			pass

def AutoFit(Sheet,ColumnNumber):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_AutoFit")
			Macro(Sheet,ColumnNumber)
			break
		except:
			pass

def WrapText(Sheet,RowStart,ColStart,RowEnd,ColEnd):
	while True:
		try:
			Macro = xl.Book(Excel_File).macro("PYTHON_WrapText")
			Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd)
			break
		except:
			pass

def PrintPlate(Sheet, StartRow, StartCol, PlateName, LabwareName, PlateRows, PlateCols, ValArray):

	CreateBorder(Sheet,StartRow,StartCol,StartRow+PlateRows,StartCol+PlateCols-1,1,3)
	CreateBorder(Sheet,StartRow+1,StartCol,StartRow+PlateRows,StartCol+PlateCols-1,1,3)
	Merge(Sheet,StartRow,StartCol,StartRow,StartCol+PlateCols-1)
	FontSize(Sheet,StartRow,StartCol,StartRow,StartCol+PlateCols-1,20)
	Center(Sheet,StartRow,StartCol,StartRow+PlateRows,StartCol+PlateCols-1)
	#Do some formatting so it looks nice

	Test = [""] * PlateRows * PlateCols
	Test = [Test[i:i+PlateCols] for i in range(0, len(Test), PlateCols)]

	for item in ValArray:
		Row = int(item) % PlateRows
		if Row == 0:
			Row = PlateRows
		Row -= 1
		Col = int((int(item) - 1) / PlateRows)

		Test[Row][Col] = str(ValArray[item]["AlphaNumeric"]) + ": " + str(ValArray[item]["Volume"]) + "uL"
	
	WriteSheet(Sheet,StartRow,StartCol,[[PlateName + ": " +LabwareName]])
	WriteSheet(Sheet, StartRow+1, StartCol, Test)

	return (PlateRows+1, PlateCols)


def PrintReagent(Sheet, StartRow, StartCol, PlateName, LabwareName, Volume):

	CreateBorder(Sheet,StartRow,StartCol,StartRow+8,StartCol+4,1,3)
	CreateBorder(Sheet,StartRow+1,StartCol,StartRow+8,StartCol+4,1,3)
	CreateBorder(Sheet,StartRow+2,StartCol,StartRow+8,StartCol+4,1,3)
	CreateBorder(Sheet,StartRow+3,StartCol,StartRow+8,StartCol+4,1,3)

	Merge(Sheet,StartRow,StartCol,StartRow,StartCol+4)
	Merge(Sheet,StartRow+1,StartCol,StartRow+1,StartCol+4)
	Merge(Sheet,StartRow+2,StartCol,StartRow+2,StartCol+4)

	FontSize(Sheet,StartRow,StartCol,StartRow,StartCol+4,14)
	FontSize(Sheet,StartRow+1,StartCol,StartRow+1,StartCol+4,12)
	FontSize(Sheet,StartRow+2,StartCol,StartRow+2,StartCol+4,12)

	Center(Sheet,StartRow,StartCol,StartRow,StartCol+4)
	Center(Sheet,StartRow+1,StartCol,StartRow+1,StartCol+4)
	Center(Sheet,StartRow+2,StartCol,StartRow+2,StartCol+4)
	#make it look nice before we write the data

	Merge(Sheet,StartRow+3,StartCol,StartRow+3,StartCol+1)
	Merge(Sheet,StartRow+4,StartCol,StartRow+4,StartCol+1)
	Merge(Sheet,StartRow+5,StartCol,StartRow+5,StartCol+1)
	Merge(Sheet,StartRow+6,StartCol,StartRow+6,StartCol+1)
	Merge(Sheet,StartRow+7,StartCol,StartRow+7,StartCol+1)
	Merge(Sheet,StartRow+8,StartCol,StartRow+8,StartCol+1)

	Merge(Sheet,StartRow+3,StartCol+2,StartRow+3,StartCol+4)
	Merge(Sheet,StartRow+4,StartCol+2,StartRow+4,StartCol+4)
	Merge(Sheet,StartRow+5,StartCol+2,StartRow+5,StartCol+4)
	Merge(Sheet,StartRow+6,StartCol+2,StartRow+6,StartCol+4)
	Merge(Sheet,StartRow+7,StartCol+2,StartRow+7,StartCol+4)
	Merge(Sheet,StartRow+8,StartCol+2,StartRow+8,StartCol+4)

	WriteSheet(Sheet,StartRow,StartCol,[[PlateName],[LabwareName],["Minimum Volume: " + str(Volume) + "uL"],["Reagent"],["Reagent Lot"],["Reagent Volume"],["Diluent"],["Diluent Lot"],["Diluent Volume"]])

	return (10,5)