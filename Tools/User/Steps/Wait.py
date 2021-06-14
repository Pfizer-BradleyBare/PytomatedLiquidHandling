from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Timer as TIMER
import time

TITLE = "Wait"
TIME = STEPS.PARAMS_START + 0

#format is Plate: WaitTime, StartTime
Timer_List = {}

def Init():
	global Timer_List

	Timer_List = {} 

#Callback is a function that takes only a plate name as a parameter (String)
def StartTimer(Plate, WaitTime, Callback):
	global Timer_List
	WaitTime *= 60

	Timer_List[Plate] = [WaitTime, time.time(), Callback]
	TIMER.Start(Plate,WaitTime)

	PLATES.GetPlate(Plate).Deactivate()

	if len(PLATES.GetActivePlates()) == 0:
		WaitForTimer()

def WaitForTimer():
	global Timer_List
	
	if STEPS.GetCurrentStep() == DESALT.GetEquilibrationStep():
		DESALT.Equilibrate()
	#It is more efficient to equilibrate when the deck is not busy. So we will do it before we wait on a incubation timer

	if len(Timer_List) > 0:

		Time = time.time()
		SleepingPlate = min(Timer_List, key=lambda x: Timer_List[x][0] - (Time - Timer_List[x][1]))

		TIMER.Wait(SleepingPlate)

		Timer_List[SleepingPlate][2](SleepingPlate)
		#Calls our callback function

		del Timer_List[SleepingPlate]

		PLATES.GetPlate(SleepingPlate).Activate()

def Callback(Plate):
	pass

def Step(step):
	StartTimer(step.GetParentPlate(), step[TIME], Callback)




