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
TEMPWAIT = "Wait For Temperature?"
TIME = "Time (min)"
SHAKE = "Shake (rpm)"
#CORRECT = "Correct For Evaporation?"

#List of all incubation steps
Incubation_List = []
#List of incubations currently in progress (heating or otherwise)
Ongoing_Incubations_List = []
AlreadyWaitingFlag = False

IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def DoesStatusUpdates():
	return True

######################################################################### 
#	Description: intialized through the following actions:
#	1. Load step specific configuration information and stores to be used later
#	2. Combines the HHS prefix with the plate sequence information and stores in a dictionary for later use. Additionally add all HHS and Lid sequences to the hamilton check sequences
#	Input Arguments: 
#	Returns: 
#########################################################################
def Init(MutableStepsList):
	global IsUsedFlag

	for Step in MutableStepsList:
		if Step.GetTitle() == TITLE:

			Params = Step.GetParameters()
			Temp = Params[TEMP]
			Time = Params[TIME]
			Shake = Params[SHAKE]

			#########################
			#########################
			#########################
			#### INPUT VALIDATION ###
			#########################
			#########################
			#########################
			MethodComments = []
			
			#Is source the destination?
			if type(Temp) is str:
				if Temp != "Ambient":
					MethodComments.append("The Temp parameter can be either \"Ambient\" or a number. Please Correct.")

			if type(Time) is str:
				MethodComments.append("The Time parameter can only be a number. Please Correct.")

			if type(Shake) is str:
				MethodComments.append("The Shake parameter can only be a number. Please Correct.")

			if len(MethodComments) != 0:
				LOG.LogMethodComment(Step,MethodComments)

			#########################
			#########################
			#########################
			#### INPUT VALIDATION ###
			#########################
			#########################
			#########################

			IsUsedFlag = True
			Incubation_List.append(Step)
	#Just finding and tracking the incubations

Before_Liquid_Handling_Incubations = {}
def StartHeatersCallback(step):
	global AlreadyWaitingFlag
	AlreadyWaitingFlag = False

	for IncubationKey in Before_Liquid_Handling_Incubations:
		Incubation = Before_Liquid_Handling_Incubations[IncubationKey]["Step"]
		Temp = Incubation.GetParameters()[TEMP]
		ParentPlate = Incubation.GetParentPlateName()

		HAMILTONIO.AddCommand(HEATER.ConfirmReservation({"PlateName":ParentPlate,"Temperature":Temp}),False)
	
	Response = HAMILTONIO.SendCommands()
	#Request the heating confirmation for all heaters

	Time = time.time()
	KeysList = list(Before_Liquid_Handling_Incubations)
	ThawKeyList = []

	for Index in range(0,len(Response)):
		Incubation = Before_Liquid_Handling_Incubations[KeysList[Index]]["Step"]
		ParentPlate = Incubation.GetParentPlateName()
		StartTime = Before_Liquid_Handling_Incubations[KeysList[Index]]["Start Time"]
		
		Before_Liquid_Handling_Incubations[KeysList[Index]]["Wait Count"] += 1
		WaitCount = Before_Liquid_Handling_Incubations[KeysList[Index]]["Wait Count"]

		if int(Response[Index]["ReturnID"]) >= 0:
			HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Reserved heater for plate name " + str(ParentPlate) + " is at temp. Proceeding"}))
			HAMILTONIO.SendCommands()
			
			ThawKeyList.append(KeysList[Index])
		
		elif (Time - StartTime) >= 60*10 or WaitCount >= 2:
			HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Unfortunately, reserved heater for plate name " + str(ParentPlate) + " has timed out. Proceeding anyway"}))
			HAMILTONIO.SendCommands()
			
			ThawKeyList.append(KeysList[Index])

	for ThawKey in ThawKeyList:
		Incubation = Before_Liquid_Handling_Incubations[ThawKey]["Step"]
		del Before_Liquid_Handling_Incubations[ThawKey]
		STEPS.ThawContext(STEPS.Class.GetContext(Incubation))
	#Iterate over all heaters and responses. Thaw the incubation contexts that are ready or have expired

	if AlreadyWaitingFlag == False and len(Before_Liquid_Handling_Incubations) != 0:
		keys = list(Before_Liquid_Handling_Incubations)
		AlreadyWaitingFlag = True
		WAIT.StartTimer(Before_Liquid_Handling_Incubations[keys[0]]["Step"],1,StartHeatersCallback, "incubator(s) to come to temp",True)
	#Finally, we want to continue waiting on heaters that need to heat as indicated by the user

def StartHeaters():
	global AlreadyWaitingFlag

	for Incubation in Incubation_List[:]:
		IncubationContext = STEPS.Class.GetContext(Incubation)

		SkipIncubation = False
		for OngoingIncubation in Ongoing_Incubations_List:
			OngoingIncubationContext = STEPS.Class.GetContext(OngoingIncubation)
			
			if OngoingIncubationContext in IncubationContext:
				SkipIncubation = True
				break
			#The ongoing incubation will always be in the same context or the parent context of the new incubation FIY.
		
		if SkipIncubation == True:
			continue
		#The way we are doing this is clever. We are always going to try to heat as many pathways as we can. 
		#However, we only want to heat one heater per pathway. So we are going to use the context to prevent multiple heating events on the same pathway.
		#We also always start from the beginning of our incubations list so if there are limited heaters, we can pause a pathway and resume when heaters are available.

		STEPS.UpdateStepParams(Incubation)

		Params = Incubation.GetParameters()
		Temp = Params[TEMP]
		RPM = Params[SHAKE]
		Wait = Params[TEMPWAIT]
		ParentPlate = Incubation.GetParentPlateName()

		if str(Temp).lower() == "Ambient".lower():
			Incubation_List.remove(Incubation)
			continue
		#If the incubation is ambient at the time we try to heat then we will remove it from the list. This is because no heaters are being used.

		HAMILTONIO.AddCommand(HEATER.AcquireReservation({"PlateName":ParentPlate,"Temperature":Temp,"RPM":RPM}),False)
		Response = HAMILTONIO.SendCommands()

		if not (Response == False) and int(Response[0]["ReturnID"]) < 0:
			STEPS.FreezeContext(IncubationContext)
			break
			#we can now break out and end starting heaters. If no heaters are available it is not worth it to try to start all following incubations
		#This is a failed command case. If an incubation fails. We need to prevent the pathway from occuring. We do not want anything to proceed until we can secure a heater.

		Incubation_List.remove(Incubation)
		Ongoing_Incubations_List.append(Incubation)

		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Reserved heater shaker / cooler for plate name " + str(ParentPlate)}))
		HAMILTONIO.SendCommands()

		if Wait.lower() == "No".lower(): #or Wait.lower() == "Before Incubation".lower():
			try:
				STEPS.ThawContext(IncubationContext)
			except:
				pass
			#It is possible that we never Froze the context. So we want to catch the error that will enivitably occur during that situation
			continue
		#Incubation has started and we do not need to wait for heating! Great! Let's try to start another heating if possible

		HAMILTONIO.AddCommand(HEATER.ConfirmReservation({"PlateName":ParentPlate,"Temperature":Temp}),True)
		Response = HAMILTONIO.SendCommands()

		if not (Response == False) and int(Response[0]["ReturnID"]) < 0:
			
			HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Heater for plate name " + str(ParentPlate) + " is not at required temp of " + str(Temp) + " C. Waiting for a max of 10 minutes before proceeding"}))
			HAMILTONIO.SendCommands()
			
			Before_Liquid_Handling_Incubations[str(STEPS.Class.GetCoordinates(Incubation))] = {"Start Time":time.time(), "Wait Count":0, "Step":Incubation}
			STEPS.FreezeContext(IncubationContext)
		#Now if the user wants to stall liquid handling it is almost always guarenteed that the temp will not be within range. 
		#We still check incase the previous and new temp are the same, but if not we will add the step to the waiting list.
		#The waiting list will wait for a max time before timeout then proceed. This ensures the temp gets close to or reaches the user set temp
	
	if AlreadyWaitingFlag == False and len(Before_Liquid_Handling_Incubations) != 0:
		AlreadyWaitingFlag = True
		keys = list(Before_Liquid_Handling_Incubations)
		WAIT.StartTimer(Before_Liquid_Handling_Incubations[keys[0]]["Step"],1,StartHeatersCallback, "incubator(s) to come to temp",True)
	#Finally, we want to continue waiting on heaters that need to heat as indicated by the user

def AmbientCallback(step):

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Performing follow up of Incubate Block. Block Coordinates: " + str(step.GetCoordinates())}))
	HAMILTONIO.SendCommands()

	ParentPlate = step.GetParentPlateName()

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Incubation for plate name " + str(ParentPlate) + " was at ambient temp. Lid will be removed"}))
	HAMILTONIO.SendCommands()

	HAMILTONIO.AddCommand(LID.GetReservationLidSequenceString({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(LID.GetReservationLidTransportType({"PlateName":ParentPlate}),False)
	#Lid

	HAMILTONIO.AddCommand(LABWARE.GetLidSequenceStrings({"PlateNames":[ParentPlate]}),False)
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

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Removing lid"}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":LidType,"SourceSequenceString":PlateLidSequence,"DestinationLabwareType":LidType,"DestinationSequenceString":LidSequence,"Park":"True","CheckExists":"After"}))
	HAMILTONIO.AddCommand(LID.ReleaseReservation({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending follow up of Incubate Block. Incubation is now complete. Block Coordinates: " + str(step.GetCoordinates())}))
	Response = HAMILTONIO.SendCommands()
	#Lets move the lid then plate then release all reservations

def HeatingCallback(step):

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Performing follow up of Incubate Block. Block Coordinates: " + str(step.GetCoordinates())}))
	HAMILTONIO.SendCommands()

	Params = step.GetParameters()
	Temp = Params[TEMP]
	RPM = Params[SHAKE]
	ParentPlate = step.GetParentPlateName()
	
	if RPM != 0:
		HeaterString = "heating and shaking"
	else:
		HeaterString = "heating"

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Incubation for plate name " + str(ParentPlate) + " required " + HeaterString + ". Removing lid then plate from heater" }))

	HAMILTONIO.AddCommand(HEATER.EndReservation({"PlateName":ParentPlate}))
	#Stop heating and shaking
	HAMILTONIO.SendCommands()

	HAMILTONIO.AddCommand(LID.GetReservationLidSequenceString({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(LID.GetReservationLidTransportType({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(HEATER.GetReservationLidSequenceString({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(HEATER.GetReservationLidTransportType({"PlateName":ParentPlate}),False)
	#Lid

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[ParentPlate]}),False)
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[ParentPlate]}),False)
	HAMILTONIO.AddCommand(HEATER.GetReservationHeaterSequenceString({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(HEATER.GetReservationHeaterTransportType({"PlateName":ParentPlate}),False)
	#Plate

	Response = HAMILTONIO.SendCommands()

	if Response == False:
		LidSequence = ""
		LidType = ""
		HeaterLidSequence = ""
		HeaterLidType = ""
	else:
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

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Removing lid"}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":HeaterLidType,"SourceSequenceString":HeaterLidSequence,"DestinationLabwareType":LidType,"DestinationSequenceString":LidSequence,"Park":"False","CheckExists":"After"}))
	Response = HAMILTONIO.SendCommands()

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Removing plate"}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":HeaterType,"SourceSequenceString":HeaterSequence,"DestinationLabwareType":PlateType,"DestinationSequenceString":PlateSequence,"Park":"True","CheckExists":"After"}))
	Response = HAMILTONIO.SendCommands()
	
	HAMILTONIO.AddCommand(HEATER.ReleaseReservation({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(LID.ReleaseReservation({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending follow up of Incubate Block. Incubation is now complete. Block Coordinates: " + str(step.GetCoordinates())}))
	Response = HAMILTONIO.SendCommands()
	#Lets move the lid then plate then release all reservations

	Ongoing_Incubations_List.remove(step)
	StartHeaters()

def Step(step):

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Starting Incubate Block. Block Coordinates: " + str(step.GetCoordinates())}))
	HAMILTONIO.SendCommands()
	
	Params = step.GetParameters()
	Temp = Params[TEMP]

	if str(Temp).lower() == "Ambient".lower():
		AmbientStep(step)
	else:
		HeatingStep(step)

def AmbientStep(step):

	Params = step.GetParameters()
	ParentPlate = step.GetParentPlateName()
	Time = step.GetParameters()[TIME]

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Incubation for plate name " + str(ParentPlate) + " is at ambient temp. Plate will be covered only"}))
	HAMILTONIO.SendCommands()

	PLATES.LABWARE.GetLabware(ParentPlate).SetIsCovered()
	#This incubation is ambient on the deck. So we set a flag which requires that the plate has a lid on deck position

	HAMILTONIO.AddCommand(LABWARE.GetLidSequenceStrings({"PlateNames":[ParentPlate]}),False)

	HAMILTONIO.AddCommand(LID.AcquireReservation({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(LID.GetReservationLidSequenceString({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(LID.GetReservationLidTransportType({"PlateName":ParentPlate}),False)
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

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Moving lid"}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":LidType,"SourceSequenceString":LidSequence,"DestinationLabwareType":LidType,"DestinationSequenceString":PlateLidSequence,"Park":"True","CheckExists":"After"}))
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Adding block to timer list to incubate for " + str(Time) + " minutes"}))
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending Incubate Block. Plate is now on incubator. Block Coordinates: " + str(step.GetCoordinates())}))

	Response = HAMILTONIO.SendCommands()
	#Lets move the plate then lid then start the incubation (Incudes shaking)
	
	WAIT.StartTimer(step, Time, AmbientCallback, "ambient Incubation of plate name" + str(ParentPlate))
	#Wait for incubation to complete.

def HeatingStep(step):

	Params = step.GetParameters()
	Temp = Params[TEMP]
	RPM = Params[SHAKE]
	Time = step.GetParameters()[TIME]
	ParentPlate = step.GetParentPlateName()

	if RPM != 0:
		HeaterString = "heating and shaking"
	else:
		HeaterString = "heating"

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Incubation for plate name " + str(ParentPlate) + " requires " + HeaterString + ". Moving plate to heater with lid" }))
	HAMILTONIO.SendCommands()

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[ParentPlate]}),False)
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[ParentPlate]}),False)
	HAMILTONIO.AddCommand(HEATER.GetReservationHeaterSequenceString({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(HEATER.GetReservationHeaterTransportType({"PlateName":ParentPlate}),False)
	#Plate

	HAMILTONIO.AddCommand(LID.AcquireReservation({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(LID.GetReservationLidSequenceString({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(LID.GetReservationLidTransportType({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(HEATER.GetReservationLidSequenceString({"PlateName":ParentPlate}),False)
	HAMILTONIO.AddCommand(HEATER.GetReservationLidTransportType({"PlateName":ParentPlate}),False)
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

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Moving plate to heater. See heater info for exact location."}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":PlateType,"SourceSequenceString":PlateSequence,"DestinationLabwareType":HeaterType,"DestinationSequenceString":HeaterSequence,"Park":"False","CheckExists":"False"}))
	Response = HAMILTONIO.SendCommands()

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Moving lid"}))
	HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":LidType,"SourceSequenceString":LidSequence,"DestinationLabwareType":HeaterLidType,"DestinationSequenceString":HeaterLidSequence,"Park":"True","CheckExists":"False"}))
	Response = HAMILTONIO.SendCommands()
	
	if RPM != 0:
		HeaterString = "heating at " + str(Temp) + " C and shaking at " + str(RPM) + " RPM"
	else:
		HeaterString = "heating at " + str(Temp) + " C and no shaking"

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Starting incubation with " + HeaterString}))
	HAMILTONIO.AddCommand(HEATER.StartReservation({"PlateName":ParentPlate,"Temperature":Temp,"RPM":RPM}))
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Adding block to timer list to incubate for " + str(Time) + " minutes"}))
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending Incubate Block. Plate is now on incubator. Block Coordinates: " + str(step.GetCoordinates())}))
	Response = HAMILTONIO.SendCommands()
	#Lets move the plate then lid then start the incubation (Incudes shaking)

	WAIT.StartTimer(step, Time, HeatingCallback, "incubation of plate name " + str(ParentPlate))
	#Wait for incubation to complete.



