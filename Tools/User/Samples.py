from ..User.Steps import Steps as STEP
from ..General import ExcelIO as EXCELIO
import copy

WORKLIST_SAMPLE_SEQUENCE = "_SampleSequence"
#Worklist constants

#This dict holds the specific range of the specified column. That way sample information can be pulled as needed.
Column_Ranges = {}

#This is the number of samples in the sheet.
Num_Samples = 0
Total_Samples = 0
#This includes sequence duplicates

#This is the sequence list, adjusted for the sample start position.
Sequences = []

######################################################################### 
#	Description: Returns the number of rows-1 or samples in the worklist
#	Input Arguments: N/A
#	Returns: Integer
#########################################################################
def GetNumSamples():
	global Num_Samples
	return Num_Samples

######################################################################### 
#	Description: Returns the number of sequences in the worklist. Sequences are described in the _SampleSequence Column
#	Input Arguments: None
#	Returns: Integer
#########################################################################
def GetTotalSamples():
	global Total_Samples
	return Total_Samples

######################################################################### 
#	Description: Returns the all sequence positions that will be used
#	Input Arguments: None
#	Returns: 1D Array of Integers
#########################################################################
def GetSequences():
	global Sequences
	return Sequences

######################################################################### 
#	Description: Performs Initialization of this module by doing the following:
#		1. Count the number of sample rows
#		2. Get the range for each column present in the worklist
#		3. Get and count the number of sequence positions
#	Input Arguments: [SampleStartPosition: Integer] [PulledWorkListSheet: List of Lists]
#	Returns: N/A
#########################################################################
def Init(SampleStartPosition, PulledWorkListSheet):
	global Num_Samples
	global Total_Samples
	global Column_Ranges
	global Sequences

	Column_Ranges = {}
	Num_Samples = 0
	Sequences = []

	Sample_Sheet = PulledWorkListSheet

	while(True):
		if Sample_Sheet[Num_Samples + 1][0] == None:
			break
		Num_Samples += 1
	#end

	count = 0
	while(True):
		Column_Name = Sample_Sheet[0][count]
		if Column_Name == None:
			break

		Column_Ranges[Column_Name] = [2,count+1,1+Num_Samples,count+1]
		count += 1
	#end

	for SampleSeq in Column(WORKLIST_SAMPLE_SEQUENCE):
		Temp = []
		for Seq in str(SampleSeq).split(","):
			Temp.append(int(float(Seq)) + SampleStartPosition - 1)
		Sequences.append(Temp)
	Total_Samples = len(Temp)

	#Temp = []
	#for row in Column("_SampleSequence"):
	#	Temp += str(row).split(",")
	#Total_Samples = len(Temp)
	#Get total number of samples, which includes duplicates. Not the same as the number of rows in worklist

######################################################################### 
#	Description: Searches the dictionary for the specified column name. If column name is not found, then the column name is returned in the array
#	Input Arguments: [Column_Name: String]
#	Returns: [List of length Num_Samples]
#########################################################################
def Column(Column_Name):
	global Column_Ranges
	global Num_Samples

	try:
		Temp = Column_Ranges[Column_Name]
		return EXCELIO.Pull(EXCELIO.WORKLIST_SHEET, Temp[0], Temp[1], Temp[2], Temp[3], 1)
	except:
		return [Column_Name] * Num_Samples
