from ..General import ExcelIO as EXCELIO
import copy

#This dict holds the specific range of the specified column. That way sample information can be pulled as needed.
Column_Ranges = {}

NumSamples = 0
def GetNumSamples():
	return NumSamples

StartPosition = 0
def GetStartPosition():
	global StartPosition
	return StartPosition

######################################################################### 
#	Description: Performs Initialization of this module by doing the following:
#		1. Count the number of sample rows
#		2. Get the range for each column present in the worklist
#		3. Get and count the number of sequence positions
#	Input Arguments: [SampleStartPosition: Integer] [PulledWorkListSheet: List of Lists]
#	Returns: N/A
#########################################################################
def Init(SampleStartPosition, PulledWorkListSheet):
	global Column_Ranges
	global StartPosition
	global NumSamples
	global SequencesList

	StartPosition = SampleStartPosition
	Column_Ranges = {}
	NumSamples = 0

	Sample_Sheet = PulledWorkListSheet

	SampleVerificationCount = 1
	while(True):
		WorklistSampleNumber = Sample_Sheet[NumSamples + 1][0]
		
		if WorklistSampleNumber == None:
			break
		elif WorklistSampleNumber != SampleVerificationCount:
			EXCELIO.CreateMessageBox("Issue found with worklist column Sample Number. Sample numbers do not increment correctly (1,2,3,4,etc.). Please Correct.", "Critical Validation Issue")
			quit()

		SampleVerificationCount += 1 
		NumSamples += 1
	#end
	
	count = 0
	while(True):
		Column_Name = Sample_Sheet[0][count]
		if Column_Name == None:
			break

		Column_Ranges[Column_Name] = [2,count+1,1+NumSamples,count+1]
		count += 1
	#end

######################################################################### 
#	Description: Searches the dictionary for the specified column name. If column name is not found, then the column name is returned in the array
#	Input Arguments: [Column_Name: String]
#	Returns: [List of length Num_Samples]
#########################################################################
def Column(Column_Name):
	global Column_Ranges
	global NumSamples

	if isinstance(Column_Name, list) == True:
		return Column_Name

	try:
		Temp = Column_Ranges[Column_Name]
		return EXCELIO.Pull(EXCELIO.WORKLIST_SHEET, Temp[0], Temp[1], Temp[2], Temp[3], 1)
	except:
		pass
	return [Column_Name] * NumSamples

def InColumn(Column_Name):

	Found = True
	try:
		Temp = Column_Ranges[Column_Name]
	except:
		Found = False
	return Found
