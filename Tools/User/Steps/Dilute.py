from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...User import Samples as SAMPLES
from ...Hamilton.Commands import Pipette as PIPETTE
from ...Hamilton.Commands import StatusUpdate as STATUS_UPDATE
from ...User import Configuration as CONFIGURATION
from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG
from ..Steps import Liquid_Transfer as LIQUID_TRANSFER
import copy

TITLE = "Dilute"
SOURCE = "Source"
DILUENT = "Diluent"
STARTING_CONCENTRATION = "Starting Concentration (mg/mL)"
TARGET_CONCENTRATION = "Target Concentration (mg/mL)"
TARGET_VOLUME = "Target Volume (uL)"
MAX_SOURCE_VOLUME = "Max Source Volume (uL)"

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
	MaxSourceVolumeList = SAMPLES.Column(step.GetParameters()[MAX_SOURCE_VOLUME])
	SourceConcentrationList = SAMPLES.Column(step.GetParameters()[STARTING_CONCENTRATION])
	SourceList = SAMPLES.Column(step.GetParameters()[SOURCE])
	DiluentList = SAMPLES.Column(step.GetParameters()[DILUENT])
	DestinationSequences = PLATES.GetPlate(step.GetParentPlate()).GetSequences()

	STATUS_UPDATE.AppendText("Transfering " + str(step.GetParameters()[TARGET_VOLUME]) + " uL of sample to " + str(step.GetParentPlate()) + " plate")

	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, SOLUTIONS.TYPE_REAGENT, SOLUTIONS.STORAGE_AMBIENT)

	for Diluent in DiluentList:
		SOLUTIONS.AddSolution(Diluent, SOLUTIONS.TYPE_BUFFER, SOLUTIONS.STORAGE_AMBIENT)

	SourceVolumeList = list(map(lambda x,y,z: (z * y) / x if x != None and x != 0 else 0, SourceConcentrationList,TargetVolumeList,TargetConcentrationList))
	DiluentVolumeList = list(map(lambda x,y: y - x, SourceVolumeList,TargetVolumeList))
	#Calculate correct volumes to pipette

	#DestinationSequences = PLATES.GetPlate(step.GetParentPlate()).GetSequenceList()

	for VolIndex in range(0,len(SourceVolumeList)):
		if MaxSourceVolumeList[VolIndex] > TargetVolumeList[VolIndex] or MaxSourceVolumeList[VolIndex] == 0:
			MaxSourceVolumeList[VolIndex] = TargetVolumeList[VolIndex]

		if SourceVolumeList[VolIndex] > MaxSourceVolumeList[VolIndex] or DiluentVolumeList[VolIndex] < 0:
			LOG.Comment("Volume is out of range for Position " + str(DestinationSequences[VolIndex]) + ". Performing automatic correction to upper and lower limits. (Source,Diluent): 0 > (" + str(SourceVolumeList[VolIndex]) + "," + str(DiluentVolumeList[VolIndex]) + ") > " + str(MaxSourceVolumeList[VolIndex]))
			SourceVolumeList[VolIndex] = MaxSourceVolumeList[VolIndex]
			DiluentVolumeList[VolIndex] = TargetVolumeList[VolIndex] - MaxSourceVolumeList[VolIndex]

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

	DestinationPlate = step.GetParentPlate()

	if PLATES.GetPlate(DestinationPlate).GetVolume() != 0:
		Mix = SAMPLES.Column("Yes")
	else:
		Mix = SAMPLES.Column("No")

	LOG.EndCommentsLog()

	FirstSequences = PLATES.GetPlate(step.GetParentPlate()).CreatePipetteSequence(FirstSourceList, FirstVolumeList,Mix)
	
	for Counter in range(0,FirstSequences.GetNumSequencePositions()):
		SOLUTIONS.GetSolution(FirstSequences.GetSources()[Counter]).AddVolume(FirstSequences.GetTransferVolumes()[Counter])
		SOLUTIONS.AddPipetteVolume(FirstSequences.GetTransferVolumes()[Counter])

	SecondSequences = PLATES.GetPlate(step.GetParentPlate()).CreatePipetteSequence(SecondSourceList, SecondVolumeList,SAMPLES.Column("Yes"))

	for Counter in range(0,SecondSequences.GetNumSequencePositions()):
		SOLUTIONS.GetSolution(SecondSequences.GetSources()[Counter]).AddVolume(SecondSequences.GetTransferVolumes()[Counter])
		SOLUTIONS.AddPipetteVolume(SecondSequences.GetTransferVolumes()[Counter])

	FirstSeqFlag = False
	if FirstSequences.GetNumSequencePositions() != 0:

		TransferVolumes = FirstSequences.GetTransferVolumes()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":len(TransferVolumes)*["Water"]}))
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}))
		FirstSeqFlag = True

	SecondSeqFlag = False
	if SecondSequences.GetNumSequencePositions() != 0:

		TransferVolumes = SecondSequences.GetTransferVolumes()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":len(TransferVolumes)*["Water"]}))
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}))
		SecondSeqFlag = True

	Response = HAMILTONIO.SendCommands()

	if Response == False:
		if FirstSeqFlag == True:
			FirstLiquidClassStrings = []
			FirstTipSequenceStrings = []

		if SecondSeqFlag == True:
			SecondLiquidClassStrings = []
			SecondTipSequenceStrings = []
	else:

		if FirstSeqFlag == True:
			FirstLiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
			FirstTipSequenceStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())

		if SecondSeqFlag == True:
			SecondLiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
			SecondTipSequenceStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())

	if FirstSeqFlag == True:
		HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":FirstSequences,"LiquidClasses":FirstLiquidClassStrings,"TipSequences":FirstTipSequenceStrings,"KeepTips":"False"}))
	
	if SecondSeqFlag == True:
		HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":SecondSequences,"LiquidClasses":SecondLiquidClassStrings,"TipSequences":SecondTipSequenceStrings,"KeepTips":"False"}))
	
	Response = HAMILTONIO.SendCommands()


	#Do the diluent pipetting
#end


