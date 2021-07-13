from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Heater_Shaker as HEATER_SHAKER
from ...Hamilton.Commands import Lid as LID
from ..Steps import Wait as WAIT
from ...User import Configuration as CONFIGURATION
import time

TITLE = "Incubate"
TEMP = "Temp (C)"
TIME = "Time (min)"
SHAKE = "Shake (rpm)"

#format is [Plate, Temp, RPM]
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
			
			Heaters[Config["Heaters"]["COM_ID"][HHS]] = {"Reserved":False, "Type":Config["Heaters"]["Type"][HHS], "Shake":Config["Heaters"]["Shake"][HHS], "Temp":25, "RPM":0}

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
		 Incubation_List.append({"Plate":Step.GetParentPlate(), "Temp":Step.GetParameters()[TEMP], "RPM":Step.GetParameters()[SHAKE]}) 

	print(Incubation_List)
	print("\n",Lids)
	print("\n",Heaters)
	StartHeaters()

def StartHeaters():
	global Incubation_List

	if len(Incubation_List) == 0:
		return

	while True:
		Temp = Incubation_List[0]
		Response = HEATER_SHAKER.Reserve(Temp["Plate"], Temp["Temp"], Temp["RPM"])

		if Response == False:
			break

		Incubation_List.remove(Temp)

def Callback(Plate):
	LID.Remove(Plate)
	LID.Release(Plate)
	HEATER_SHAKER.Remove(Plate)
	HEATER_SHAKER.Release(Plate)

	StartHeaters()

def Step(step):
	Plate = step.GetParentPlate()
	Temp = step.GetParameters()[TEMP]
	if str(Temp).lower() == "ambient":
		PLATES.GetPlate(Plate).SetLidState()

	HEATER_SHAKER.Move(Plate)
	LID.Reserve(Plate)
	LID.Move(Plate)
	
	WAIT.StartTimer(Plate, step.GetParameters()[TIME], Callback)



