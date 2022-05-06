from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Timer as TIMER
from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG
import time

TITLE = "Wait"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

#format is Plate: WaitTime, StartTime
Timer_List = {}

def Init():
	global Timer_List

	Timer_List = [] 

#Callback is a function that takes only a plate name as a parameter (String)
def StartTimer(step, WaitTime, Callback):
	global Timer_List
	WaitTime *= 60
	#Convert min to seconds

	Timer_List.append( {"Step":step,"Wait Time":WaitTime, "Start Time":time.time(), "Callback":Callback})
	#TIMER.Start(Plate,WaitTime)
	#We will only start the time for the remaining time. Time handling will be done in python

	STEPS.DeactivateContext(step.GetContext())

	if len(STEPS.GetActiveContexts()) == 0:
		WaitForTimer()

def WaitForTimer():
	global Timer_List
	
	if len(Timer_List) > 0:	
		CurrentStep = Timer_List[-1]["Step"]

		Params = DESALT.GetDesaltParams()
		for key in Params:
			if Params[key]["EQ Step"] == CurrentStep:
				DESALT.Equilibrate(key)
		#It is more efficient to equilibrate when the deck is not busy. So we will do it before we wait on a incubation timer



		Time = time.time()

		SleepingPlate = min(Timer_List, key=lambda x: x["Wait Time"] - (Time - x["Start Time"]))
		
		HAMILTONIO.AddCommand(TIMER.Start({"WaitTime":SleepingPlate["Wait Time"] - (Time - SleepingPlate["Start Time"])}))
		HAMILTONIO.AddCommand(TIMER.Wait({}))
		Response = HAMILTONIO.SendCommands()

		Timer_List.remove(SleepingPlate)

		STEPS.ActivateContext(SleepingPlate["Step"].GetContext())

		SleepingPlate["Callback"](SleepingPlate["Step"])
		#Calls our callback function



def Callback(step):
	pass

def Step(step):
	LOG.BeginCommentsLog()
	StartTimer(step.GetParentPlate(), step[TIME], Callback)
	LOG.EndCommentsLog()




