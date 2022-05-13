
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

def CreateSheet(Sheet):
	xl.Book(Excel_File).sheets.add(Sheet,after="Solutions")

def DeleteSheet(Sheet):
	xl.Book(Excel_File).sheets[Sheet].delete()

def Pull(Sheet, RowStart, ColStart, RowEnd, ColEnd, n=1):
	if Excel_File == None:
		print("ExcelIO -- Init First")
		return None
	else: 
		return xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).options(ndim=n).value

#
# Reading a sheet is easy. For Excel 2010, if you try to write a sheet while a save is ongoing is crashes the xlwings app. By using a macro it never crashes
#
def WriteSheet(Sheet,Row,Col,Text2DArray):
	Macro = xl.Book(Excel_File).macro("PYTHON_WriteSheet")
	Macro(Sheet,Row,Col,Text2DArray)

def GetMethod():
	return Pull(METHOD_SHEET, METHOD_ROW_START, METHOD_COL_START, METHOD_ROW_END, METHOD_COL_END,2)

def GetWorklist():
	return Pull(WORKLIST_SHEET, WORKLIST_ROW_START, WORKLIST_COL_START, WORKLIST_ROW_END, WORKLIST_COL_END,2)

def GetMethodValidatedStatus():
	Macro = xl.Book(Excel_File).macro("Python_GetMethodValidatedStatus")
	Macro()
	return Pull("BuildingBlocks",1,1,1,1)[0]

def CreateMessageBox(Message, Title):
	Macro = xl.Book(Excel_File).macro("PYTHON_CreateMessageBox")
	Macro(Message, Title)

def SelectCell(Sheet,Row,Col):
	Macro = xl.Book(Excel_File).macro("PYTHON_SelectCell")
	Macro(Sheet,Row,Col)

def CreateBorder(Sheet,RowStart,ColStart,RowEnd,ColEnd,BorderStyle,BorderWeight):
	Macro = xl.Book(Excel_File).macro("PYTHON_CreateBorder")
	Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd)

def Merge(Sheet,RowStart,ColStart,RowEnd,ColEnd):
	Macro = xl.Book(Excel_File).macro("PYTHON_Merge")
	Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd)

def FontSize(Sheet,RowStart,ColStart,RowEnd,ColEnd, FontSize):
	Macro = xl.Book(Excel_File).macro("PYTHON_FontSize")
	Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd, FontSize)

def Center(Sheet,RowStart,ColStart,RowEnd,ColEnd):
	Macro = xl.Book(Excel_File).macro("PYTHON_Center")
	Macro(Sheet,RowStart,ColStart,RowEnd,ColEnd)

def AutoFit(Sheet,ColumnNumber):
	Macro = xl.Book(Excel_File).macro("PYTHON_AutoFit")
	Macro(Sheet,ColumnNumber)

def PrintPlate(StartRow, StartCol, PlateName, LabwareName, PlateRows, PlateCols, ValArray):

	CreateBorder("PrepList",StartRow,StartCol,StartRow+PlateRows,StartCol+PlateCols-1,1,3)
	CreateBorder("PrepList",StartRow+1,StartCol,StartRow+PlateRows,StartCol+PlateCols-1,1,3)
	Merge("PrepList",StartRow,StartCol,StartRow,StartCol+PlateCols-1)
	FontSize("PrepList",StartRow,StartCol,StartRow,StartCol+PlateCols-1,20)
	Center("PrepList",StartRow,StartCol,StartRow+PlateRows,StartCol+PlateCols-1)
	#make it look nice before we write the data

	TitleString = PlateName + ": " +LabwareName
	WriteSheet("PrepList",StartRow,StartCol,[[TitleString]])
	#Push("PrepList",StartRow,StartCol,StartRow,StartCol, TitleString)
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
	
	#Push("PrepList", StartRow+1, StartCol, StartRow+1, StartCol, Test)
	WriteSheet("PrepList", StartRow+1, StartCol, Test)

	return (PlateRows+1, PlateCols)


def PrintReagent(StartRow, StartCol, PlateName, LabwareName, Volume):

	CreateBorder("PrepList",StartRow,StartCol,StartRow+8,StartCol+4,1,3)
	CreateBorder("PrepList",StartRow+1,StartCol,StartRow+8,StartCol+4,1,3)
	CreateBorder("PrepList",StartRow+2,StartCol,StartRow+8,StartCol+4,1,3)
	CreateBorder("PrepList",StartRow+3,StartCol,StartRow+8,StartCol+4,1,3)

	Merge("PrepList",StartRow,StartCol,StartRow,StartCol+4)
	Merge("PrepList",StartRow+1,StartCol,StartRow+1,StartCol+4)
	Merge("PrepList",StartRow+2,StartCol,StartRow+2,StartCol+4)

	FontSize("PrepList",StartRow,StartCol,StartRow,StartCol+4,14)
	FontSize("PrepList",StartRow+1,StartCol,StartRow+1,StartCol+4,12)
	FontSize("PrepList",StartRow+2,StartCol,StartRow+2,StartCol+4,12)

	Center("PrepList",StartRow,StartCol,StartRow,StartCol+4)
	Center("PrepList",StartRow+1,StartCol,StartRow+1,StartCol+4)
	Center("PrepList",StartRow+2,StartCol,StartRow+2,StartCol+4)
	#make it look nice before we write the data

	#Push("PrepList",StartRow,StartCol,StartRow,StartCol, PlateName)
	#Push("PrepList",StartRow+1,StartCol,StartRow+1,StartCol, LabwareName)
	#Push("PrepList",StartRow+2,StartCol,StartRow+2,StartCol, "Minimum Volume: " + str(round(Volume,2)) + "uL")

	WriteSheet("PrepList",StartRow,StartCol,PlateName)
	WriteSheet("PrepList",StartRow+1,StartCol,LabwareName)
	WriteSheet("PrepList",StartRow+2,StartCol,"Minimum Volume: " + str(round(Volume,2)) + "uL")

	Merge("PrepList",StartRow+3,StartCol,StartRow+3,StartCol+1)
	Merge("PrepList",StartRow+4,StartCol,StartRow+4,StartCol+1)
	Merge("PrepList",StartRow+5,StartCol,StartRow+5,StartCol+1)
	Merge("PrepList",StartRow+6,StartCol,StartRow+6,StartCol+1)
	Merge("PrepList",StartRow+7,StartCol,StartRow+7,StartCol+1)
	Merge("PrepList",StartRow+8,StartCol,StartRow+8,StartCol+1)

	Merge("PrepList",StartRow+3,StartCol+2,StartRow+3,StartCol+4)
	Merge("PrepList",StartRow+4,StartCol+2,StartRow+4,StartCol+4)
	Merge("PrepList",StartRow+5,StartCol+2,StartRow+5,StartCol+4)
	Merge("PrepList",StartRow+6,StartCol+2,StartRow+6,StartCol+4)
	Merge("PrepList",StartRow+7,StartCol+2,StartRow+7,StartCol+4)
	Merge("PrepList",StartRow+8,StartCol+2,StartRow+8,StartCol+4)

	#Push("PrepList",StartRow+3,StartCol,StartRow+3,StartCol+1, "Reagent")
	#Push("PrepList",StartRow+4,StartCol,StartRow+4,StartCol+1, "Reagent Lot")
	#Push("PrepList",StartRow+5,StartCol,StartRow+5,StartCol+1, "Reagent Volume")
	#Push("PrepList",StartRow+6,StartCol,StartRow+6,StartCol+1, "Diluent")
	#Push("PrepList",StartRow+7,StartCol,StartRow+7,StartCol+1, "Diluent Lot")
	#Push("PrepList",StartRow+8,StartCol,StartRow+8,StartCol+1, "Diluent Volume")

	WriteSheet("PrepList",StartRow+3,StartCol,"Reagent")
	WriteSheet("PrepList",StartRow+4,StartCol,"Reagent Lot")
	WriteSheet("PrepList",StartRow+5,StartCol,"Reagent Volume")
	WriteSheet("PrepList",StartRow+6,StartCol,"Diluent")
	WriteSheet("PrepList",StartRow+7,StartCol,"Diluent Lot")
	WriteSheet("PrepList",StartRow+8,StartCol,"Diluent Volume")

	return (10,5)