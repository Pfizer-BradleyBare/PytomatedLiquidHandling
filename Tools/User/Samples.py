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

def GetNumSamples():
	global Num_Samples
	return Num_Samples

def GetTotalSamples():
	global Total_Samples
	return Total_Samples

def GetSequences():
	global Sequences
	return Sequences

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

	Temp = []
	for row in Column("_SampleSequence"):
		Temp += str(row).split(",")
	Total_Samples = len(Temp)
	#Get total number of samples, which includes duplicates. Not the same as the number of rows in worklist

def Column(Column_Name):
	global Column_Ranges
	global Num_Samples

	try:
		Temp = Column_Ranges[Column_Name]
		return EXCELIO.Pull(EXCELIO.WORKLIST_SHEET, Temp[0], Temp[1], Temp[2], Temp[3], 1)
	except:
		return [Column_Name] * Num_Samples
