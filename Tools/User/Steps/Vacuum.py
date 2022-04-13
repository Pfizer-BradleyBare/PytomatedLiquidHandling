from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ..Steps import Plate as PLATE
from ..Steps import Liquid_Transfer as LIQUID_TRANSFER
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...Hamilton.Commands import Transport as TRANSPORT
from ...Hamilton.Commands import Labware as LABWARE
from ...Hamilton.Commands import Vacuum as VACUUM
from ...Hamilton.Commands import Pipette as PIPETTE
from ...User import Configuration as CONFIGURATION
from ...General import Log as LOG
from ...General import HamiltonIO as HAMILTONIO

TITLE = "Vacuum"
SOURCE = "Source"
VOLUME = "Volume (uL)"
VACUUM_PLATE = "Vacuum Plate"
WAIT_TIME = "Pre Vacuum Wait (min)"
PRESSURE = "Pressure Difference (mTorr)"
TIME = "Vacuum Time (min)"

IsUsedFlag = False
VacPlates = set()

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def GetVacPlates():
	global VacPlates
	return VacPlates

def Init(MutableStepsList, SequencesList):
	global IsUsedFlag
	global VacPlates

	for Step in MutableStepsList:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			VacPlates.add(Step.GetParameters()[VACUUM_PLATE])
			CONFIGURATION.AddOmitLoading(Step.GetParameters()[VACUUM_PLATE])

def Step(step):

	Destination = step.GetParentPlate()
	SourceList = SAMPLES.Column(step.GetParameters()[SOURCE])
	VolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])
	WaitTime = step.GetParameters()[WAIT_TIME]
	VacPlate = step.GetParameters()[VACUUM_PLATE]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	PLATES.GetPlate(step.GetParentPlate()).SetVacuumState(VacPlate)
	#The plate that we vacuum into needs to be a vacuum compatible plate. Set that here on a per step basis

	Sequence = PLATES.GetPlate(Destination).CreatePipetteSequence(SourceList, VolumeList, SAMPLES.Column("No"))
	#we are going to create the sequence here so we can get all associated info at once.
	
	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, SOLUTIONS.TYPE_REAGENT, SOLUTIONS.STORAGE_AMBIENT)

	for Counter in range(0,Sequence.GetNumSequencePositions()):
		SOLUTIONS.GetSolution(Sequence.GetSources()[Counter]).AddVolume(Sequence.GetTransferVolumes()[Counter])
		SOLUTIONS.AddPipetteVolume(Sequence.GetTransferVolumes()[Counter])
	#keep tabs on all used solutions, and pipetted volumes

	LiquidTransferFlag = False
	if Sequence.GetNumSequencePositions() != 0:
		TransferVolumes = Sequence.GetTransferVolumes()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":len(TransferVolumes)*["Water"]}))
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}))
		LiquidTransferFlag = True

	HAMILTONIO.AddCommand(VACUUM.GetVacuumPlateSequenceString({"VacuumPlateName":VacPlate}))

	if not (TITLE in STEPS.GetPreviousStepInPathway(step).GetTitle()):
		
		HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[Destination]}))
		HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[Destination]}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumCollectionPlateSequenceString({"VacuumPlateName":VacPlate}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumCollectionPlateTransportType({"VacuumPlateName":VacPlate}))
		#Get info to move collection plate

		HAMILTONIO.AddCommand(VACUUM.GetVacuumParkSequenceString({"VacuumPlateName":VacPlate}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumParkTransportType({"VacuumPlateName":VacPlate}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumManifoldSequenceString({"VacuumPlateName":VacPlate}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumManifoldTransportType({"VacuumPlateName":VacPlate}))
		#Get info to move vacuum manifold
		
		Response = HAMILTONIO.SendCommands()

		if Response == False:
			ResponseHolder = False
			DeckPlateSequence = ""
			DeckPlateType = ""
			CollectionPlateSequence = ""
			CollectionPlateType = ""
			VacuumParkSequence = ""
			VacuumParkType = ""
			VacuumManifoldSequence = ""
			VacuumManifoldType = ""
		else:
			ResponseHolder = []
			if LiquidTransferFlag == True:
				ResponseHolder.append(Response.pop(0))
				ResponseHolder.append(Response.pop(0))
			ResponseHolder.append(Response.pop(0))
			DeckPlateSequence = Response.pop(0)["Response"]
			DeckPlateType = Response.pop(0)["Response"]
			CollectionPlateSequence = Response.pop(0)["Response"]
			CollectionPlateType = Response.pop(0)["Response"]
			VacuumParkSequence = Response.pop(0)["Response"]
			VacuumParkType = Response.pop(0)["Response"]
			VacuumManifoldSequence = Response.pop(0)["Response"]
			VacuumManifoldType = Response.pop(0)["Response"]
		#Lets get the info we need to move everything
		
		Response = ResponseHolder

		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":DeckPlateType,"SourceSequenceString":DeckPlateSequence,"DestinationLabwareType":CollectionPlateType,"DestinationSequenceString":CollectionPlateSequence,"Park":"False","CheckExists":"After"}))
		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":VacuumParkType,"SourceSequenceString":VacuumParkSequence,"DestinationLabwareType":VacuumManifoldType,"DestinationSequenceString":VacuumManifoldSequence,"Park":"True","CheckExists":"False"}))
		#Move collection plate then manifold
	else:
		Response = HAMILTONIO.SendCommands()

	if Response == False:
		LiquidClassStrings = ""
		TipSequenceStrings = ""
		VacuumPlateSequence = ""
	else:
		if LiquidTransferFlag == True:
			LiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
			TipSequenceStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
		VacuumPlateSequence = Response.pop(0)["Response"]

	for Counter in range(0,Sequence.GetNumSequencePositions()):
		Sequence.GetDestinations()[Counter] = VacuumPlateSequence
		Sequence.GetCurrentDestinationVolumes()[Counter] = 0
	#We need to modify the destination to be the vacuum plate sequence above. The liquid needs to move through the vacuum plate.
	#We additionally need to modify the CurrentDestinationVolume to be zero since the vacuum plate should always be zero.
	if Sequence.GetNumSequencePositions() != 0:
		HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":Sequence,"LiquidClasses":LiquidClassStrings,"TipSequences":TipSequenceStrings,"KeepTips":"False","DestinationPipettingOffset":8}))
		Response = HAMILTONIO.SendCommands()
	#This will perform the move of the collection plate, manifold (If required) and finally pipette liquid into the vacuum plate.

	WAIT.StartTimer(step,WaitTime,PreVacuumWaitCallback)
	#Vacuum wait time

def PreVacuumWaitCallback(step):
	Destination = step.GetParentPlate()
	Volume = step.GetParameters()[VOLUME]
	VacPlate = step.GetParameters()[VACUUM_PLATE]
	WaitTime = step.GetParameters()[WAIT_TIME]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	HAMILTONIO.AddCommand(VACUUM.Start({"VacuumPlateName":VacPlate,"VacuumPressure":Pressure}))
	Response = HAMILTONIO.SendCommands()

	WAIT.StartTimer(step,Time,VacuumWaitCallback)
	#Wait for vacuum time now

def VacuumWaitCallback(step):

	Destination = step.GetParentPlate()
	Volume = step.GetParameters()[VOLUME]
	VacPlate = step.GetParameters()[VACUUM_PLATE]
	WaitTime = step.GetParameters()[WAIT_TIME]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	HAMILTONIO.AddCommand(VACUUM.Stop({"VacuumPlateName":VacPlate}))
	Response = HAMILTONIO.SendCommands()
	
	if not (TITLE in STEPS.GetNextStepInPathway(step).GetTitle()):

		HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[Destination]}))
		HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[Destination]}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumCollectionPlateSequenceString({"VacuumPlateName":VacPlate}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumCollectionPlateTransportType({"VacuumPlateName":VacPlate}))
		#Get info to move collection plate

		HAMILTONIO.AddCommand(VACUUM.GetVacuumParkSequenceString({"VacuumPlateName":VacPlate}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumParkTransportType({"VacuumPlateName":VacPlate}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumManifoldSequenceString({"VacuumPlateName":VacPlate}))
		HAMILTONIO.AddCommand(VACUUM.GetVacuumManifoldTransportType({"VacuumPlateName":VacPlate}))
		#Get info to move vacuum manifold
		
		Response = HAMILTONIO.SendCommands()

		if Response == False:
			DeckPlateSequence = ""
			DeckPlateType = ""
			CollectionPlateSequence = ""
			CollectionPlateType = ""
			VacuumParkSequence = ""
			VacuumParkType = ""
			VacuumManifoldSequence = ""
			VacuumManifoldType = ""
		else:
			DeckPlateSequence = Response.pop(0)["Response"]
			DeckPlateType = Response.pop(0)["Response"]
			CollectionPlateSequence = Response.pop(0)["Response"]
			CollectionPlateType = Response.pop(0)["Response"]
			VacuumParkSequence = Response.pop(0)["Response"]
			VacuumParkType = Response.pop(0)["Response"]
			VacuumManifoldSequence = Response.pop(0)["Response"]
			VacuumManifoldType = Response.pop(0)["Response"]
		#Lets get the info we need to move everything

		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":VacuumManifoldType,"SourceSequenceString":VacuumManifoldSequence,"DestinationLabwareType":VacuumParkType,"DestinationSequenceString":VacuumParkSequence,"Park":"False","CheckExists":"False"}))
		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":CollectionPlateType,"SourceSequenceString":CollectionPlateSequence,"DestinationLabwareType":DeckPlateType,"DestinationSequenceString":DeckPlateSequence,"Park":"True","CheckExists":"After"}))
		Response = HAMILTONIO.SendCommands()
		#Move collection plate then manifold
