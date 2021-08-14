from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...User import Samples as SAMPLES
from ...Hamilton.Commands import Pipette as PIPETTE
from ...User import Configuration as CONFIGURATION
from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG
import copy

TITLE = "Dilute"
SOURCE = "Source"
DILUENT = "Diluent"
STARTING_CONCENTRATION = "Starting Concentration (mg/mL)"
TARGET_CONCENTRATION = "Target Concentration (mg/mL)"
TARGET_VOLUME = "Target Volume (uL)"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

######################################################################### 
#	Description: No itialization required here. Provided for consistency
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Init():
	pass

######################################################################### 
#	Description: Performs a dilution step by doing the following:
#	1. Forms a pipette hamilton command for the diluent solution
#	2. Forms a pipette hamilton command for the source solution
#	Input Arguments: [step: Step class]
#	Returns: N/A
#########################################################################
def Step(step):
	#dilute equation is C1*V1 = C2*V2 Where:
	#C1 is SourceConcentration
	#V1 is Source Volume
	#C2 is Target Concentration
	#V2 is Target Volume
	#We need to solve for Source Volume
	#V1 = (C2*V2)/C1

	LOG.BeginCommentsLog()

	TargetConcentrationList = SAMPLES.Column(step.GetParameters()[TARGET_CONCENTRATION])
	TargetVolumeList = SAMPLES.Column(step.GetParameters()[TARGET_VOLUME])
	SourceConcentrationList = SAMPLES.Column(step.GetParameters()[STARTING_CONCENTRATION])
	SourceList = SAMPLES.Column(step.GetParameters()[SOURCE])
	DiluentList = SAMPLES.Column(step.GetParameters()[DILUENT])

	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, SOLUTIONS.TYPE_REAGENT, SOLUTIONS.STORAGE_AMBIENT)

	for Diluent in DiluentList:
		SOLUTIONS.AddSolution(Diluent, SOLUTIONS.TYPE_BUFFER, SOLUTIONS.STORAGE_AMBIENT)

	SourceVolumeList = list(map(lambda x,y,z: (z * y) / x if x != None and x != 0 else 0, SourceConcentrationList,TargetVolumeList,TargetConcentrationList))
	DiluentVolumeList = list(map(lambda x,y: y - x, SourceVolumeList,TargetVolumeList))
	#Calculate correct volumes to pipette

	DestinationSequences = PLATES.GetPlate(step.GetParentPlate()).GetSequenceList()

	for VolIndex in range(0,len(SourceVolumeList)):
		if SourceVolumeList[VolIndex] > TargetVolumeList[VolIndex] or DiluentVolumeList[VolIndex] < 0:
			LOG.Comment("Volume is out of range for Position " + str(DestinationSequences[VolIndex]) + ". Performing automatic correction to upper and lower limits. (Source,Diluent): 0 > (" + str(SourceVolumeList[VolIndex]) + "," + str(DiluentVolumeList[VolIndex]) + ") > " + str(TargetVolumeList[VolIndex]))
			SourceVolumeList[VolIndex] = TargetVolumeList[VolIndex]
			DiluentVolumeList[VolIndex] = 0

		if DiluentVolumeList[VolIndex] > TargetVolumeList[VolIndex] or SourceVolumeList[VolIndex] < 0:
			LOG.Comment("Volume is out of range for Position " + str(DestinationSequences[VolIndex]) + ". Performing automatic correction to upper and lower limits. (Source,Diluent): 0 > (" + str(SourceVolumeList[VolIndex]) + "," + str(DiluentVolumeList[VolIndex]) + ") > " + str(TargetVolumeList[VolIndex]))
			DiluentVolumeList[VolIndex] = TargetVolumeList[VolIndex]
			SourceVolumeList[VolIndex] = 0
	#check for ridiculous pipetting volumes and correct it. User should ideally never input something ridiculous

	FirstSourceList = []
	FirstVolumeList = []
	SecondSourceList = []
	SecondVolumeList = []

	for index in range(0,len(SourceVolumeList)):
		if SourceVolumeList[index] > DiluentVolumeList[index]:
			FirstSourceList.append(SourceList[index])
			FirstVolumeList.append(SourceVolumeList[index])

			SecondSourceList.append(DiluentList[index])
			SecondVolumeList.append(DiluentVolumeList[index])
		else:
			SecondSourceList.append(SourceList[index])
			SecondVolumeList.append(SourceVolumeList[index])
			
			FirstSourceList.append(DiluentList[index])
			FirstVolumeList.append(DiluentVolumeList[index])
	#We want to pipette the highest volume first for each sample no matter what.

	LOG.EndCommentsLog()

	LOG.BeginCommentsLog()
	DestinationPlate = step.GetParentPlate()

	if PLATES.GetPlate(DestinationPlate).GetVolume() != 0:
		Mix = SAMPLES.Column("Yes")
	else:
		Mix = SAMPLES.Column("No")

	Sequences = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(FirstSourceList, FirstVolumeList, Mix)

	_Temp = copy.deepcopy(Sequences)
	for Sequence in _Temp:
		SOLUTIONS.GetSolution(Sequence["Source"]).AddVolume(Sequence["Volume"])
		SOLUTIONS.AddPipetteVolume(Sequence["Volume"])

	if HAMILTONIO.IsSimulated() == False:
		for sequence in Sequences:
			sequence["Source"] = CONFIGURATION.GetDeckLoading(sequence["Source"])["Sequence"]
			sequence["Destination"] = CONFIGURATION.GetDeckLoading(sequence["Destination"])["Sequence"]
		DestinationPlate = CONFIGURATION.GetDeckLoading(DestinationPlate)["Sequence"]



	if len(Sequences) == 0:
		LOG.Comment("Number of sequences is zero so no liquid transfer will actually occur.")

	LOG.EndCommentsLog()

	LOG.BeginCommandLog()
	if len(Sequences) != 0:
		PIPETTE.Do(DestinationPlate, Sequences)
	LOG.EndCommandLog()
	#Do the source pipetting

	LOG.BeginCommentsLog()
	DestinationPlate = step.GetParentPlate()

	Sequences = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(SecondSourceList, SecondVolumeList, SAMPLES.Column("Yes"))

	_Temp = copy.deepcopy(Sequences)
	for Sequence in _Temp:
		SOLUTIONS.GetSolution(Sequence["Source"]).AddVolume(Sequence["Volume"])
		SOLUTIONS.AddPipetteVolume(Sequence["Volume"])

	if HAMILTONIO.IsSimulated() == False:
		for sequence in Sequences:
			sequence["Source"] = CONFIGURATION.GetDeckLoading(sequence["Source"])["Sequence"]
			sequence["Destination"] = CONFIGURATION.GetDeckLoading(sequence["Destination"])["Sequence"]
		DestinationPlate = CONFIGURATION.GetDeckLoading(DestinationPlate)["Sequence"]

	if len(Sequences) == 0:
		LOG.Comment("Number of sequences is zero so no liquid transfer will actually occur.")

	LOG.EndCommentsLog()

	LOG.BeginCommandLog()
	if len(Sequences) != 0:
		PIPETTE.Do(DestinationPlate, Sequences)
	LOG.EndCommandLog()
	#Do the diluent pipetting
#end


