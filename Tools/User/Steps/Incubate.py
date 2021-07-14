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

######################################################################### 
#	Description: intialized through the following actions:
#	1. Load step specific configuration information and stores to be used later
#	2. Combines the HHS prefix with the plate sequence information and stores in a dictionary for later use. Additionally add all HHS and Lid sequences to the hamilton check sequences
#	Input Arguments: 
#	Returns: 
#########################################################################
def Init(MutableStepsList):
	global Incubation_List

	Config = CONFIGURATION.GetStepConfig(TITLE)

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
		if Step.GetTitle() == TITLE and str(Step.GetParameters()[TEMP]).lower() != "Ambient".lower():
			Incubation_List.append(Step)

	print(Incubation_List)
	print("\n",Lids)
	print("\n",Heaters,"\n\n")
	StartHeaters()

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
	

	Lids[Lid]["Reserved"] = False

	if ID != None:
		Heaters[ID]["Reserved"] = False
		HEATER.StopHeating(ID)
		HEATER.StopShaking(ID)
		TRANSPORT.Move(1,2,3,4)
		#Move lid
		TRANSPORT.Move(1,2,3,4)
		#Move the plate back
	else:
		TRANSPORT.Move(1,2,3,4)
		#Move lid

	StartHeaters()

def Step(step):
	ID = GetReservedHeater(step)

	if ReserveLid(step) == False:
		WAIT.WaitForTimer()
	#We need to wait for incubation to finish if no lids are available

	Lid = GetReservedLid(step)

	if ID != None:
		TRANSPORT.Move(1,2,3,4)
		#Move the plate to the heater if not ambient incubation
		
		TRANSPORT.Move(1,2,3,4)
		#Move lid
		
		HEATER.StartShaking(ID, step.GetParameters()[SHAKE])

	else:
		PLATES.GetPlate(step.GetParentPlate()).SetLidState()
		#This is a RT incubation on a carrier so we need to record that for deck loading
		
		TRANSPORT.Move(1,2,3,4)
		#Move lid
	
	WAIT.StartTimer(step, step.GetParameters()[TIME], Callback)



