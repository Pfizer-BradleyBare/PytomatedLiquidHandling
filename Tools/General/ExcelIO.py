
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

def CreateSheet(Sheet):
	xl.Book(Excel_File).sheets.add(Sheet,after="Worklist")

def DeleteSheet(Sheet):
	xl.Book(Excel_File).sheets[Sheet].delete()

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

def CreateBorder(Sheet,RowStart,ColStart,RowEnd,ColEnd,BorderStyle,BorderWeight):

	Range = xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd))

	Range.api.borders(9).LineStyle = BorderStyle
	Range.api.borders(9).Weight = BorderWeight
	Range.api.borders(7).LineStyle = BorderStyle
	Range.api.borders(7).Weight = BorderWeight
	Range.api.borders(8).LineStyle = BorderStyle
	Range.api.borders(8).Weight = BorderWeight
	Range.api.borders(10).LineStyle = BorderStyle
	Range.api.borders(10).Weight = BorderWeight

def Merge(Sheet,RowStart,ColStart,RowEnd,ColEnd):
	xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).merge()

def FontSize(Sheet,RowStart,ColStart,RowEnd,ColEnd, FontSize):
	xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).api.Font.Size = FontSize

def Center(Sheet,RowStart,ColStart,RowEnd,ColEnd):
	xl.Book(Excel_File).sheets[Sheet].range((RowStart,ColStart),(RowEnd,ColEnd)).api.HorizontalAlignment = -4108

def AutoFit(Sheet):
	xl.Book(Excel_File).sheets[Sheet].autofit()

def PrintPlate(StartRow, StartCol, PlateName, LabwareName, PlateRows, PlateCols, ValArray):

	CreateBorder("PrepList",StartRow,StartCol,StartRow+PlateRows,StartCol+PlateCols-1,1,3)
	CreateBorder("PrepList",StartRow+1,StartCol,StartRow+PlateRows,StartCol+PlateCols-1,1,3)
	Merge("PrepList",StartRow,StartCol,StartRow,StartCol+PlateCols-1)
	FontSize("PrepList",StartRow,StartCol,StartRow,StartCol+PlateCols-1,20)
	Center("PrepList",StartRow,StartCol,StartRow+PlateRows,StartCol+PlateCols-1)
	#make it look nice before we write the data

	TitleString = PlateName + ": " +LabwareName
	Push("PrepList",StartRow,StartCol,StartRow,StartCol+PlateCols-1, TitleString)
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
	
	Push("PrepList", StartRow+1, StartCol, StartRow+1, StartCol, Test)

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

	Push("PrepList",StartRow,StartCol,StartRow,StartCol+4, PlateName)
	Push("PrepList",StartRow+1,StartCol,StartRow+1,StartCol+4, LabwareName)
	Push("PrepList",StartRow+2,StartCol,StartRow+2,StartCol+4, "Minimum Volume: " + str(round(Volume,2)) + "uL")

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

	Push("PrepList",StartRow+3,StartCol,StartRow+3,StartCol+1, "Reagent")
	Push("PrepList",StartRow+4,StartCol,StartRow+4,StartCol+1, "Reagent Lot")
	Push("PrepList",StartRow+5,StartCol,StartRow+5,StartCol+1, "Reagent Volume")
	Push("PrepList",StartRow+6,StartCol,StartRow+6,StartCol+1, "Diluent")
	Push("PrepList",StartRow+7,StartCol,StartRow+7,StartCol+1, "Diluent Lot")
	Push("PrepList",StartRow+8,StartCol,StartRow+8,StartCol+1, "Diluent Volume")

	return (10,5)