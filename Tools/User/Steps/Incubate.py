from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Heater as HEATER
from ...Hamilton.Commands import Transport as TRANSPORT
from ..Steps import Wait as WAIT
from ..Steps import Split_Plate as SPLIT_PLATE
from ...User import Configuration as CONFIGURATION
from ...General import Log as LOG
import time

TITLE = "Incubate"
TEMP = "Temp (C)"
TIME = "Time (min)"
SHAKE = "Shake (rpm)"

#List of incubation steps
Incubation_List = []
Incubation_Num_List = []

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

				PlateSequence = Config["Heaters"]["SequencePrefix"][HHS] + Config["Heaters"]["PlateSequences"][PlateType]
				LidSequence = Config["Heaters"]["SequencePrefix"][HHS] + Config["Heaters"]["LidSequences"][PlateType]
				Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"][PlateType]["Plate"] = PlateSequence
				Heaters[Config["Heaters"]["COM_ID"][HHS]]["Sequences"][PlateType]["Lid"] = LidSequence
				CONFIGURATION.AddCheckSequence(PlateSequence)
				CONFIGURATION.AddCheckSequence(LidSequence)
	#This does double duty. It combines the sequence prefix with the plate and lid sequences. In doing so it also ensures that each plate sequence has a matching lid sequence, which is imperative.
	#Do configuration for the incubation step

	IncubationCounter = 1

	for Step in MutableStepsList:
		if Step.GetTitle() == SPLIT_PLATE.TITLE:
			IncubationCounter += 1


		if Step.GetTitle() == TITLE:
			
			IsUsedFlag = True

			if str(Step.GetParameters()[TEMP]).lower() != "Ambient".lower():
					Incubation_List.append(Step)
					Incubation_Num_List.append(IncubationCounter)

	print(Incubation_List)
	print(Incubation_Num_List)
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

		NumReservedHeaters = 0
		for Heater in Heaters:
			if (not not Heaters[Heater]["Reserved"]) == True:
				NumReservedHeaters += 1
		if not(NumReservedHeaters < Incubation_Num_List[0]):
			return
		#Only heat the number of plates we have running at one time

		for ID in PossibleHeaters:
			if (not not Heaters[ID]["Reserved"]) == False and (not not Incubation.GetParameters()[SHAKE]) <= Heaters[ID]["Shake"]:

				Heaters[ID]["Reserved"] = Incubation
				Incubation_List.pop(0)
				Incubation_Num_List.pop(0)
				Heaters[ID]["Temp"] = Temp

				LOG.BeginCommandLog()
				HEATER.StartHeating(ID,Temp)
				LOG.EndCommandLog()
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
		
		LOG.BeginCommandLog()
		HEATER.StopHeating(ID)
		LOG.EndCommandLog()


		if step.GetParameters()[SHAKE] > 0:
			LOG.BeginCommandLog()
			HEATER.StopShaking(ID)
			LOG.EndCommandLog()
		
		if Loading != None:
			LidTransportDestination = Lid
			LidTransportSource = Heaters[ID]["Sequences"][Loading["Labware Name"]]["Lid"]
			LidTransportOpenDistance = TransportConfig["Lid"]["Open"]
			LidTransportCloseDistance = TransportConfig["Lid"]["Close"]
			#Lid

			PlateTransportDestination = Loading["Sequence"]
			PlateTransportSource = Heaters[ID]["Sequences"][Loading["Labware Name"]]["Plate"]
			PlateTransportOpenDistance = TransportConfig[Loading["Labware Name"]]["Open"]
			PlateTransportCloseDistance = TransportConfig[Loading["Labware Name"]]["Close"]
			#plate
			LOG.BeginCommandLog()
			TRANSPORT.Move(LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance,0)
			LOG.EndCommandLog()
			LOG.BeginCommandLog()
			TRANSPORT.Move(PlateTransportSource,PlateTransportDestination,PlateTransportOpenDistance,PlateTransportCloseDistance,1)
			LOG.EndCommandLog()
		

	else:
		if Loading != None:
			LidTransportDestination = Lid
			LidTransportSource = Loading["Lid"]
			LidTransportOpenDistance = TransportConfig["Lid"]["Open"]
			LidTransportCloseDistance = TransportConfig["Lid"]["Close"]
			LOG.BeginCommandLog()
			TRANSPORT.Move(LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance, 1)
			LOG.EndCommandLog()

	StartHeaters()

def Step(step):
	global Heaters
	global TransportConfig
	LOG.BeginCommentsLog()
	LOG.EndCommentsLog()
	while ReserveLid(step) == False:
		WAIT.WaitForTimer()
	#We need to wait for incubation to finish if no lids are available

	ID = GetReservedHeater(step)
	Lid = GetReservedLid(step)
	Loading = CONFIGURATION.GetDeckLoading(step.GetParentPlate())

	if ID != None:
		if Loading != None:
			PlateTransportSource = Loading["Sequence"]
			PlateTransportDestination = Heaters[ID]["Sequences"][Loading["Labware Name"]]["Plate"]
			PlateTransportOpenDistance = TransportConfig[Loading["Labware Name"]]["Open"]
			PlateTransportCloseDistance = TransportConfig[Loading["Labware Name"]]["Close"]
			#plate
		
			LidTransportSource = Lid
			LidTransportDestination = Heaters[ID]["Sequences"][Loading["Labware Name"]]["Lid"]
			LidTransportOpenDistance = TransportConfig["Lid"]["Open"]
			LidTransportCloseDistance = TransportConfig["Lid"]["Close"]
			#Lid
			LOG.BeginCommandLog()
			TRANSPORT.Move(PlateTransportSource,PlateTransportDestination,PlateTransportOpenDistance,PlateTransportCloseDistance,0)
			LOG.EndCommandLog()
			LOG.BeginCommandLog()
			TRANSPORT.Move(LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance,1)
			LOG.EndCommandLog()

		if step.GetParameters()[SHAKE] > 0:
			LOG.BeginCommandLog()
			HEATER.StartShaking(ID, step.GetParameters()[SHAKE])
			LOG.EndCommandLog()
	else:
		if Loading != None:
			LidTransportSource = Lid
			LidTransportDestination = Loading["Lid"]
			LidTransportOpenDistance = TransportConfig["Lid"]["Open"]
			LidTransportCloseDistance = TransportConfig["Lid"]["Close"]
			LOG.BeginCommandLog()
			TRANSPORT.Move(LidTransportSource,LidTransportDestination,LidTransportOpenDistance,LidTransportCloseDistance, 1)
			LOG.EndCommandLog()
		
		PLATES.GetPlate(step.GetParentPlate()).SetLidState()
	#Make decisions if incubation is ambient or not
	
	WAIT.StartTimer(step, step.GetParameters()[TIME], Callback)



