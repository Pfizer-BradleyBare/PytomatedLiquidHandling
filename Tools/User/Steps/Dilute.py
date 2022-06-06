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
	return IsUsedFlag

def Init():
	pass

def Step(step):
	#dilute equation is C1*V1 = C2*V2 Where:
	#C1 is SourceConcentration
	#V1 is Source Volume
	#C2 is Target Concentration
	#V2 is Target Volume
	#We need to solve for Source Volume
	#V1 = (C2*V2)/C1

	StepParameters = STEPS.Class.GetParameters(step)
	TargetConcentrationList = SAMPLES.Column(StepParameters[TARGET_CONCENTRATION])
	TargetVolumeList = SAMPLES.Column(StepParameters[TARGET_VOLUME])
	MaxSourceVolumeList = SAMPLES.Column(StepParameters[MAX_SOURCE_VOLUME])
	SourceConcentrationList = SAMPLES.Column(StepParameters[STARTING_CONCENTRATION])
	SourceList = SAMPLES.Column(StepParameters[SOURCE])
	DiluentList = SAMPLES.Column(StepParameters[DILUENT])
	Destination = STEPS.Class.GetParentPlateName(step)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []
	
	#Is source the destination?
	if Destination in SourceList:
		MethodComments.append("The Source parameter and parent plate (Destination) are the same. This doesn't make sense. Please correct.")

	#Is diluent the destination?
	if Destination in DiluentList:
		MethodComments.append("The Diluent parameter and parent plate (Destination) are the same. This doesn't make sense. Please correct.")

	#Testing Source
	if not all(type(Source) is str for Source in SourceList):
		MethodComments.append("The Source parameter you provided is a number. This parameter must contain letters. Please Correct")

	#Testing DILUENT
	if not all(type(Diluent) is str for Diluent in DiluentList):
		MethodComments.append("The Diluent parameter you provided is a number. This parameter must contain letters. Please Correct")

	DoTest = True
	#Testing Target Conc
	if not all(not (type(Conc) is str) for Conc in TargetConcentrationList):
		MethodComments.append("The Target Concentration parameter you provided is not a number. This parameter must be a number. Please Correct")
		DoTest = False

	#Testing Starting Conc
	if not all(not (type(Conc) is str) for Conc in SourceConcentrationList):
		MethodComments.append("The Source Concentration parameter you provided is not a number. This parameter must be a number. Please Correct")
		DoTest = False

	#Testing Starting and Target Concentration
	if DoTest == True and not all(SourceConcentration == 0 for SourceConcentration in SourceConcentrationList) and not all(TargetConcentration <= SourceConcentration for SourceConcentration,TargetConcentration in zip(SourceConcentrationList,TargetConcentrationList)):
		MethodComments.append("Source Concentration must be greater than Target Concentration for a proper dilution. Please Correct.")	

	DoTest = True
	#Testing Target Volume
	if not all(not (type(TargetVolume) is str) for TargetVolume in TargetVolumeList):
		MethodComments.append("The Target Volume parameter you provided is not a number. This parameter must be a number. Please Correct")
		DoTest = False

	#Testing Max Source Volume
	if not all(not (type(MaxSourceVolume) is str) for MaxSourceVolume in MaxSourceVolumeList):
		MethodComments.append("The Max Source Volume parameter you provided is not a number. This parameter must be a number. Please Correct")
		DoTest = False

	#Testing Target and max source volume
	if DoTest == True and not all(MaxSourceVolume <= TargetVolume for MaxSourceVolume,TargetVolume in zip(MaxSourceVolumeList,TargetVolumeList)):
		MethodComments.append("Max Source Volume can not be greater than Target Volume. Please Correct")	

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	SourceVolumeList = list(map(lambda x,y,z: (z * y) / x if x != None and x != 0 else 0, SourceConcentrationList,TargetVolumeList,TargetConcentrationList))
	DiluentVolumeList = list(map(lambda x,y: y - x, SourceVolumeList,TargetVolumeList))
	#Calculate correct volumes to pipette

	DestinationNames = SAMPLES.Column(Destination)
	DestinationContextStrings = PLATES.LABWARE.GetContextualStringsList(step, DestinationNames)

	for VolIndex in range(0,len(SourceVolumeList)):
		if MaxSourceVolumeList[VolIndex] > TargetVolumeList[VolIndex] or MaxSourceVolumeList[VolIndex] == 0:
			MaxSourceVolumeList[VolIndex] = TargetVolumeList[VolIndex]

		if SourceVolumeList[VolIndex] > MaxSourceVolumeList[VolIndex] or DiluentVolumeList[VolIndex] < 0:
			#LOG.Comment("Volume is out of range for Position " + str(SAMPLES.GetContextualSequences(DestinationContextStrings[VolIndex])[VolIndex]) + ". Performing automatic correction to upper and lower limits. (Source): 0 < " + str(SourceVolumeList[VolIndex]) + " < " + str(MaxSourceVolumeList[VolIndex]))
			SourceVolumeList[VolIndex] = MaxSourceVolumeList[VolIndex]
			DiluentVolumeList[VolIndex] = TargetVolumeList[VolIndex] - MaxSourceVolumeList[VolIndex]

		if DiluentVolumeList[VolIndex] > TargetVolumeList[VolIndex] or SourceVolumeList[VolIndex] < 0:
			#LOG.Comment("Volume is out of range for Position " + str(SAMPLES.GetContextualSequences(DestinationContextStrings[VolIndex])[VolIndex]) + ". Performing automatic correction to upper and lower limits. (Source): 0 < " + str(SourceVolumeList[VolIndex]) + " < " + str(TargetVolumeList[VolIndex]))
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

	FirstSourceContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,FirstSourceList)
	SecondSourceContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,SecondSourceList)

	FirstSequences = PLATES.CreatePipetteSequence(DestinationContextStrings, DestinationNames, FirstSourceContextualStrings, FirstSourceList, FirstVolumeList,SAMPLES.Column("No"))

	SecondSequences = PLATES.CreatePipetteSequence(DestinationContextStrings, DestinationNames, SecondSourceContextualStrings, SecondSourceList, SecondVolumeList,SAMPLES.Column("Dispense:10"))

	FirstSeqFlag = False
	if FirstSequences.GetNumSequencePositions() != 0:

		TransferVolumes = FirstSequences.GetTransferVolumes()
		LiquidClassStrings = FirstSequences.GetLiquidClassStrings()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":LiquidClassStrings}),False)
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}),False)
		FirstSeqFlag = True

	SecondSeqFlag = False
	if SecondSequences.GetNumSequencePositions() != 0:

		TransferVolumes = SecondSequences.GetTransferVolumes()
		LiquidClassStrings = SecondSequences.GetLiquidClassStrings()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":LiquidClassStrings}),False)
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}),False)
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
		HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":FirstSequences,"LiquidClasses":FirstLiquidClassStrings,"TipSequences":FirstTipSequenceStrings,"KeepTips":"False","DestinationPipettingOffset":0}))
		Response = HAMILTONIO.SendCommands()

	if SecondSeqFlag == True:
		HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":SecondSequences,"LiquidClasses":SecondLiquidClassStrings,"TipSequences":SecondTipSequenceStrings,"KeepTips":"False","DestinationPipettingOffset":0}))
		Response = HAMILTONIO.SendCommands()

	#Do the diluent pipetting
#end


