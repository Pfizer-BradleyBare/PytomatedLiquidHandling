from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Heater as HEATER
from ...Hamilton.Commands import Transport as TRANSPORT
from ..Steps import Wait as WAIT
from ...User import Configuration as CONFIGURATION
import time

TITLE = "Incubate"
TEMP = "Temp (C)"
TIME = "Time (min)"
SHAKE = "Shake (rpm)"

#List of incubation steps
Incubation_List = []

Lids = {}
Heaters = {}
TransportConfig = {}

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
	global Heaters
	global Lids
	global TransportConfig
	global IsUsedFlag


	Config = CONFIGURATION.GetStepConfig(TITLE)
	TransportConfig = CONFIGURATION.GetStepConfig("Transport")

	for Lid in Config["LidHomeSequences"]:
		Lids[Lid] = {"Reserved": False}
		CONFIGURATION.AddCheckSequence(Lid)

	if "Heaters" in Config:
		for HHS in range(0,len(Config["Heaters"]["COM_ID"])):
			
			Heaters[Config["Heaters"]["COM_ID"][HHS]] = {"Reserved":False, "Type":Config["Heaters"]["Type"][HHS], "Shake":Config["Heaters"]["Shake"][HHS], "Temp":25}

			Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"] = {}
			for PlateType in Config["Heaters"]["PlateSequences"]:

				Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"][PlateType] = {}
				for PlateVol in Config["Heaters"]["PlateSequences"][PlateType]:

					Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"][PlateType][PlateVol] = {}
					Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"][PlateType][PlateVol]["Plate"] = {}
					Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"][PlateType][PlateVol]["Lid"] = {}
					PlateSequence = Config["Heaters"]["SequencePrefix"][HHS] + Config["Heaters"]["PlateSequences"][PlateType][PlateVol]
					LidSequence = Config["Heaters"]["SequencePrefix"][HHS] + Config["Heaters"]["LidSequences"][PlateType][PlateVol]
					Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"][PlateType][PlateVol]["Plate"] = PlateSequence
					Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"][PlateType][PlateVol]["Lid"] = LidSequence
					CONFIGURATION.AddCheckSequence(PlateSequence)
					CONFIGURATION.AddCheckSequence(LidSequence)
	#This does double duty. It combines the sequence prefix with the plate and lid sequences. In doing so it also ensures that each plate sequence has a matching lid sequence, which is imperative.
	#Do configuration for the incubation step

	for Step in MutableStepsList:
		if Step.GetTitle() == TITLE:
			
			IsUsedFlag = True

			if str(Step.GetParameters()[TEMP]).lower() != "Ambient".lower():
					Incubation_List.append(Step)

	print(Incubation_List)
	print("\n",Lids)
	print("\n",Heaters,"\n\n")
	StartHeaters()

def GetHeaterList():
	HeaterList = []
	for Heater in Heaters:
		HeaterList.append({"ID":Heater, "Type":Heaters[Heater]["Type"]})
	return HeaterList

def StartHeaters():
	global Incubation_List
	global Heaters

	for Incubation in Incubation_List[:]:
		Temp = Incubation.GetParameters()[TEMP]
		PossibleHeaters = sorted(Heaters, key=lambda h: abs(Heaters[h]["Temp"] - Temp))

		for ID in PossibleHeaters:
			if (not not Heaters[ID]["Reserved"]) == False and (not not Incubation.GetParameters()[SHAKE]) <= Heaters[ID]["Shake"]:

				Heaters[ID]["Reserved"] = Incubation
				Incubation_List.remove(Incubation)
				Heaters[ID]["Temp"] = Temp
				HEATER.StartHeating(ID,Temp)
				break

def GetReservedHeater(step):
	global Heaters
	for Heater in Heaters:
		if Heaters[Heater]["Reserved"] == step:
			return Heater
	return None

def ReserveLid(step):
	global Lids
	for Lid in Lids:
		if (not not Lids[Lid]["Reserved"]) == False:
			Lids[Lid]["Reserved"] = step
			return True
	return False

def GetReservedLid(step):
	global Lids
	for Lid in Lids:
		if Lids[Lid]["Reserved"] == step:
			return Lid
	return None

def Callback(step):
	global Heaters
	global Lids

	ID = GetReservedHeater(step)
	Lid = GetReservedLid(step)
	Loading = CONFIGURATION.GetDeckLoading(step.GetParentPlate())
	
	Lids[Lid]["Reserved"] = False

	if ID != None:
		Heaters[ID]["Reserved"] = False
		HEATER.StopHeating(ID)
		if step.GetParameters()[SHAKE] > 0:
			HEATER.StopShaking(ID)
		
		if Loading != None:
			LidTransportDestination = Lid
			LidTransportSource = Heaters[ID]["Sequences"][Loading["Labware Type"]][Loading["Max Volume"]]["Lid"]
			LidTransportOpenDistance = TransportConfig["Lid"]["Open"]
			LidTransportCloseDistance = TransportConfig["Lid"]["Close"]
			#TRANSPORT.Move(TransportSource,TransportDestination,TransportOpenDistance,TransportCloseDistance)
			#Lid

			PlateTransportDestination = Loading["Sequence"]
			PlateTransportSource = Heaters[ID]["Sequences"][Loading["Labware Type"]][Loading["Max Volume"]]["Plate"]
			PlateTransportOpenDistance = TransportConfig[Loading["Labware Type"]][Loading["Max Volume"]]["Open"]
			PlateTransportCloseDistance = TransportConfig[Loading["Labware Type"]][Loading["Max Volume"]]["Close"]
			#TRANSPORT.Move(TransportSource,TransportDestination,TransportOpenDistance,TransportCloseDistance)
			#plate

			TRANSPORT.Move(LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance,0)
			TRANSPORT.Move(PlateTransportSource,PlateTransportDestination,PlateTransportOpenDistance,PlateTransportCloseDistance,1)
			#TRANSPORT.HeaterRemove(PlateTransportSource,PlateTransportDe,stination,PlateTransportOpenDistance,PlateTransportCloseDistance,LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance)
		

	else:
		if Loading != None:
			LidTransportDestination = Lid
			LidTransportSource = Loading["Lid"]
			LidTransportOpenDistance = TransportConfig["Lid"]["Open"]
			LidTransportCloseDistance = TransportConfig["Lid"]["Close"]
			TRANSPORT.Move(LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance, 1)

	StartHeaters()

def Step(step):
	global Heaters
	global TransportConfig

	while ReserveLid(step) == False:
		WAIT.WaitForTimer()
	#We need to wait for incubation to finish if no lids are available

	ID = GetReservedHeater(step)
	Lid = GetReservedLid(step)
	Loading = CONFIGURATION.GetDeckLoading(step.GetParentPlate())

	if ID != None:
		if Loading != None:
			PlateTransportSource = Loading["Sequence"]
			PlateTransportDestination = Heaters[ID]["Sequences"][Loading["Labware Type"]][Loading["Max Volume"]]["Plate"]
			PlateTransportOpenDistance = TransportConfig[Loading["Labware Type"]][Loading["Max Volume"]]["Open"]
			PlateTransportCloseDistance = TransportConfig[Loading["Labware Type"]][Loading["Max Volume"]]["Close"]
			#TRANSPORT.Move(TransportSource,TransportDestination,TransportOpenDistance,TransportCloseDistance)
			#plate
		
			LidTransportSource = Lid
			LidTransportDestination = Heaters[ID]["Sequences"][Loading["Labware Type"]][Loading["Max Volume"]]["Lid"]
			LidTransportOpenDistance = TransportConfig["Lid"]["Open"]
			LidTransportCloseDistance = TransportConfig["Lid"]["Close"]
			#TRANSPORT.Move(TransportSource,TransportDestination,TransportOpenDistance,TransportCloseDistance)
			#Lid

			TRANSPORT.Move(PlateTransportSource,PlateTransportDestination,PlateTransportOpenDistance,PlateTransportCloseDistance,0)
			TRANSPORT.Move(LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance,1)
			#TRANSPORT.HeaterMove(PlateTransportSource,PlateTransportDestination,PlateTransportOpenDistance,PlateTransportCloseDistance,LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance)

		if step.GetParameters()[SHAKE] > 0:
			HEATER.StartShaking(ID, step.GetParameters()[SHAKE])
	else:
		if Loading != None:
			LidTransportSource = Lid
			LidTransportDestination = Loading["Lid"]
			LidTransportOpenDistance = TransportConfig["Lid"]["Open"]
			LidTransportCloseDistance = TransportConfig["Lid"]["Close"]
			TRANSPORT.Move(LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance, 1)
		
		PLATES.GetPlate(step.GetParentPlate()).SetLidState()
	#Make decisions if incubation is ambient or not
	
	WAIT.StartTimer(step, step.GetParameters()[TIME], Callback)



