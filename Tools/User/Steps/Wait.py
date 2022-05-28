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
	return IsUsedFlag

#format is Plate: WaitTime, StartTime
Timer_List = []

def Init():
	global Timer_List
	Timer_List = [] 

#Callback is a function that takes only a plate name as a parameter (String)
#Wait only means it is ONLY a timer. No other type of parallel processing will be attempted.
def StartTimer(step, WaitTime, Callback, WaitOnly=False):
	WaitTime *= 60
	#Convert min to seconds

	Timer_List.append( {"Step":step,"Wait Time":WaitTime, "Start Time":time.time(), "Callback":Callback, "Wait Only":WaitOnly})
	#We will only start the time for the remaining time. Time handling will be done in python

	if WaitOnly == False:
		STEPS.DeactivateContext(step.GetContext())

	if STEPS.GetNumActiveContexts() == 0:
		WaitForTimer()

def GetLowestTimer():
	Time = time.time()
	return min(Timer_List, key=lambda x: x["Wait Time"] - (Time - x["Start Time"]))


def WaitForTimer():
	global Timer_List
	
	if len(Timer_List) > 0:	

		Params = DESALT.GetDesaltParams()
		for Timer in Timer_List:
			if Timer["Wait Only"] == False:
				for key in Params:
					if Params[key]["EQ Step"] == Timer["Step"]:
						DESALT.Equilibrate(key)
		#It is more efficient to equilibrate when the deck is not busy. So we will do it before we wait on a incubation timer

		LowestTimer = GetLowestTimer()
		
		RemainingTime = LowestTimer["Wait Time"] - (time.time() - LowestTimer["Start Time"])

		if RemainingTime > 0:
			HAMILTONIO.AddCommand(TIMER.Start({"WaitTime":RemainingTime}), not LowestTimer["Wait Only"])
			HAMILTONIO.AddCommand(TIMER.Wait({}), not LowestTimer["Wait Only"])
			Response = HAMILTONIO.SendCommands()

		Timer_List.remove(LowestTimer)

		if LowestTimer["Wait Only"] == False:
			STEPS.ActivateContext(LowestTimer["Step"].GetContext())

		LowestTimer["Callback"](LowestTimer["Step"])
		#Calls our callback function

def CheckForExpiredTimers():
	if len(Timer_List) > 0:	
		LowestTimer = GetLowestTimer()
		if LowestTimer["Wait Time"] - (time.time() - LowestTimer["Start Time"]) <= 0:

			Timer_List.remove(LowestTimer)

			if LowestTimer["Wait Only"] == False:
				STEPS.ActivateContext(LowestTimer["Step"].GetContext())

			LowestTimer["Callback"](LowestTimer["Step"])
			#Calls our callback function

def Callback(step):
	pass

def Step(step):
	StartTimer(step.GetParentPlate(), step[TIME], Callback)




