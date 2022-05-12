from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Heater as HEATER
from ...Hamilton.Commands import Transport as TRANSPORT
from ...Hamilton.Commands import StatusUpdate as STATUS_UPDATE
from ...Hamilton.Commands import Labware as LABWARE
from ...Hamilton.Commands import Lid as LID
from ...User import Samples as SAMPLES
from ..Steps import Wait as WAIT
from ..Steps import Split_Plate as SPLIT_PLATE
from ...User import Configuration as CONFIGURATION
from ...General import Log as LOG
from ...General import HamiltonIO as HAMILTONIO

import time

TITLE = "Incubate"
TEMP = "Temp (C)"
TIME = "Time (min)"
SHAKE = "Shake (rpm)"
#CORRECT = "Correct For Evaporation?"


#List of incubation steps
Incubation_List = []
Incubation_Num_List = []
NumSimultaneousIncubations = None
CurrentIncubationIDCounter = 0

IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

######################################################################### 
#	Description: intialized through the following actions:
#	1. Load step specific configuration information and stores to be used later
#	2. Combines the HHS prefix with the plate sequence information and stores in a dictionary for later use. Additionally add all HHS and Lid sequences to the hamilton check sequences
#	Input Arguments: 
#	Returns: 
#########################################################################
def Init(MutableStepsList):
	global Incubation_List
	global Incubation_Num_List
	global IsUsedFlag
	global NumSimultaneousIncubations

	IncubationCounter = 1

	for Step in MutableStepsList:
		if Step.GetTitle() == SPLIT_PLATE.TITLE:
			IncubationCounter += 1

		if Step.GetTitle() == TITLE:
			
			IsUsedFlag = True
			
			Incubation_List.append(Step)
			Incubation_Num_List.append(IncubationCounter)

	NumSimultaneousIncubations = IncubationCounter

	StartHeaters()

OngoingIncubationsCounter = 0

def StartHeaters():
	global Incubation_List
	global Incubation_Num_List
	global OngoingIncubationsCounter
	global CurrentIncubationIDCounter

	while(len(Incubation_List) != 0):
		Incubation = Incubation_List.pop(0)
		MaxNumIncubations = Incubation_Num_List.pop(0)

		Params = Incubation.GetParameters()
		Temp = Params[TEMP]
		RPM = Params[SHAKE]
		ParentPlate = Incubation.GetParentPlateName()

		if str(Temp).lower() != "Ambient".lower():
			HAMILTONIO.AddCommand(HEATER.AcquireReservation({"PlateName":ParentPlate,"Temperature":Temp,"RPM":RPM}),False)
			Response = HAMILTONIO.SendCommands()

			CurrentIncubationIDCounter += 1
			OngoingIncubationsCounter += 1

		if OngoingIncubationsCounter == MaxNumIncubations:
			break



def AmbientCallback(step):

	ParentPlate = step.GetParentPlateName()

	HAMILTONIO.AddCommand(LID.GetReservationLidSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(LID.GetReservationLidTransportType({"PlateName":ParentPlate}))
	#Lid

	HAMILTONIO.AddCommand(LABWARE.GetLidSequenceStrings({"PlateNames":[ParentPlate]}))
	#Plate

	Response = HAMILTONIO.SendCommands()

	if Response == False:
		LidSequence = ""
		LidType = ""
		PlateLidSequence = ""
	else:
		LidSequence = Response.pop(0)["Response"]
		LidType = Response.pop(0)["Response"]
		PlateLidSequence = Response.pop(0)["Response"]
	#Lets get the info we need to move the Lid

	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":LidType,"SourceSequenceString":PlateLidSequence,"DestinationLabwareType":LidType,"DestinationSequenceString":LidSequence,"Park":"True","CheckExists":"After"}))
	HAMILTONIO.AddCommand(LID.ReleaseReservation({"PlateName":ParentPlate}))
	Response = HAMILTONIO.SendCommands()
	#Lets move the lid then plate then release all reservations

def HeatingCallback(step):

	global OngoingIncubationsCounter

	Params = step.GetParameters()
	Temp = Params[TEMP]
	RPM = Params[SHAKE]
	ParentPlate = step.GetParentPlateName()
	
	HAMILTONIO.AddCommand(HEATER.EndReservation({"PlateName":ParentPlate}))
	#Stop heating and shaking

	HAMILTONIO.AddCommand(LID.GetReservationLidSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(LID.GetReservationLidTransportType({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(HEATER.GetReservationLidSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(HEATER.GetReservationLidTransportType({"PlateName":ParentPlate}))
	#Lid

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[ParentPlate]}))
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[ParentPlate]}))
	HAMILTONIO.AddCommand(HEATER.GetReservationHeaterSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(HEATER.GetReservationHeaterTransportType({"PlateName":ParentPlate}))
	#Plate

	Response = HAMILTONIO.SendCommands()

	if Response == False:
		LidSequence = ""
		LidType = ""
		HeaterLidSequence = ""
		HeaterLidType = ""
	else:
		Response.pop(0) #This discards the EndReservation command response.
		LidSequence = Response.pop(0)["Response"]
		LidType = Response.pop(0)["Response"]
		HeaterLidSequence = Response.pop(0)["Response"]
		HeaterLidType = Response.pop(0)["Response"]
	#Lets get the info we need to move the Lid

	if Response == False:
		PlateSequence = ""
		PlateType = ""
		HeaterSequence = ""
		HeaterType = ""
	else:
		PlateSequence = Response.pop(0)["Response"]
		PlateType = Response.pop(0)["Response"]
		HeaterSequence = Response.pop(0)["Response"]
		HeaterType = Response.pop(0)["Response"]
	#Lets get the info we need to move the plate

	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":HeaterLidType,"SourceSequenceString":HeaterLidSequence,"DestinationLabwareType":LidType,"DestinationSequenceString":LidSequence,"Park":"False","CheckExists":"After"}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":HeaterType,"SourceSequenceString":HeaterSequence,"DestinationLabwareType":PlateType,"DestinationSequenceString":PlateSequence,"Park":"True","CheckExists":"After"}))
	HAMILTONIO.AddCommand(HEATER.ReleaseReservation({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(LID.ReleaseReservation({"PlateName":ParentPlate}))
	Response = HAMILTONIO.SendCommands()
	#Lets move the lid then plate then release all reservations
	
	OngoingIncubationsCounter -= 1
	StartHeaters()

def Step(step):
	LOG.BeginCommentsLog()
	LOG.EndCommentsLog()
	
	STATUS_UPDATE.AppendText("Incubate at " + str(step.GetParameters()[TEMP]) + " C for " + str(step.GetParameters()[TIME]) + " min")
	
	Params = step.GetParameters()
	Temp = Params[TEMP]

	if str(Temp).lower() == "Ambient".lower():
		AmbientStep(step)
	else:
		HeatingStep(step)

def AmbientStep(step):

	Params = step.GetParameters()
	Temp = Params[TEMP]
	ParentPlate = step.GetParentPlateName()

	PLATES.LABWARE.GetLabware(ParentPlate).SetIsCovered()
	#This incubation is ambient on the deck. So we set a flag which requires that the plate has a lid on deck position

	HAMILTONIO.AddCommand(LABWARE.GetLidSequenceStrings({"PlateNames":[ParentPlate]}))

	HAMILTONIO.AddCommand(LID.AcquireReservation({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(LID.GetReservationLidSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(LID.GetReservationLidTransportType({"PlateName":ParentPlate}))
	#Lid

	Response = HAMILTONIO.SendCommands()

	if Response == False:
		PlateLidSequence = ""
		LidSequence = ""
		LidType = ""
	else:
		PlateLidSequence = Response.pop(0)["Response"]
		Response.pop(0) #This discards the lid reservation response.
		LidSequence = Response.pop(0)["Response"]
		LidType = Response.pop(0)["Response"]
	#Lets get the info we need to move the plate

	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":LidType,"SourceSequenceString":LidSequence,"DestinationLabwareType":LidType,"DestinationSequenceString":PlateLidSequence,"Park":"True","CheckExists":"After"}))
	Response = HAMILTONIO.SendCommands()
	#Lets move the plate then lid then start the incubation (Incudes shaking)
	
	WAIT.StartTimer(step, step.GetParameters()[TIME], AmbientCallback)
	#Wait for incubation to complete.

def HeatingStep(step):

	Params = step.GetParameters()
	Temp = Params[TEMP]
	RPM = Params[SHAKE]
	ParentPlate = step.GetParentPlateName()

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[ParentPlate]}))
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[ParentPlate]}))
	HAMILTONIO.AddCommand(HEATER.GetReservationHeaterSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(HEATER.GetReservationHeaterTransportType({"PlateName":ParentPlate}))
	#Plate

	HAMILTONIO.AddCommand(LID.AcquireReservation({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(LID.GetReservationLidSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(LID.GetReservationLidTransportType({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(HEATER.GetReservationLidSequenceString({"PlateName":ParentPlate}))
	HAMILTONIO.AddCommand(HEATER.GetReservationLidTransportType({"PlateName":ParentPlate}))
	#Lid

	Response = HAMILTONIO.SendCommands()

	if Response == False:
		PlateSequence = ""
		PlateType = ""
		HeaterSequence = ""
		HeaterType = ""
	else:
		PlateSequence = Response.pop(0)["Response"]
		PlateType = Response.pop(0)["Response"]
		HeaterSequence = Response.pop(0)["Response"]
		HeaterType = Response.pop(0)["Response"]
	#Lets get the info we need to move the plate

	if Response == False:
		LidSequence = ""
		LidType = ""
		HeaterLidSequence = ""
		HeaterLidType = ""
	else:
		Response.pop(0) #This discards the lid reservation response.
		LidSequence = Response.pop(0)["Response"]
		LidType = Response.pop(0)["Response"]
		HeaterLidSequence = Response.pop(0)["Response"]
		HeaterLidType = Response.pop(0)["Response"]
	#Lets get the info we need to move the Lid

	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":PlateType,"SourceSequenceString":PlateSequence,"DestinationLabwareType":HeaterType,"DestinationSequenceString":HeaterSequence,"Park":"False","CheckExists":"False"}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":LidType,"SourceSequenceString":LidSequence,"DestinationLabwareType":HeaterLidType,"DestinationSequenceString":HeaterLidSequence,"Park":"True","CheckExists":"False"}))
	HAMILTONIO.AddCommand(HEATER.StartReservation({"PlateName":ParentPlate,"Temperature":Temp,"RPM":RPM}))
	Response = HAMILTONIO.SendCommands()
	#Lets move the plate then lid then start the incubation (Incudes shaking)
	
	WAIT.StartTimer(step, step.GetParameters()[TIME], HeatingCallback)
	#Wait for incubation to complete.



