from ..Steps import Steps as STEPS
from ..Steps import Desalt as DESALT
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Timer as TIMER
from ...General import HamiltonIO as HAMILTONIO
from ...Hamilton.Commands import StatusUpdate as STATUS_UPDATE
from ...General import Log as LOG
import time

TITLE = "Pause"
TIME = "Time (min)"

IsUsedFlag = True

def IsUsed():
	return IsUsedFlag

def DoesStatusUpdates():
	return True

#format is Plate: WaitTime, StartTime
Timer_List = []

def Init():
	global Timer_List
	Timer_List = [] 

#Callback is a function that takes only a plate name as a parameter (String)
#Wait only means it is ONLY a timer. No other type of parallel processing will be attempted.
def StartTimer(step, WaitTime, Callback, WaitReasonString, WaitOnly=False):
	WaitTime *= 60
	#Convert min to seconds

	Timer_List.append( {"Step":step,"Wait Time":WaitTime, "Start Time":time.time(), "Callback":Callback, "Wait Reason": WaitReasonString, "Wait Only":WaitOnly})
	#We will only start the time for the remaining time. Time handling will be done in python

	if WaitOnly == False:
		STEPS.DeactivateContext(step.GetContext())

	WaitForTimer()

def GetLowestTimer():
	Time = time.time()
	return min(Timer_List, key=lambda x: x["Wait Time"] - (Time - x["Start Time"]))

def WaitForTimer():
	if STEPS.GetNumActiveContexts() != 0 and not all(Context in STEPS.FrozenContextTracker for Context in STEPS.ActiveContextTracker):
		return

	if len(Timer_List) > 0:	

		HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "No pathways are currently active. Starting to wait for timer with lowest remaining time."}),False,True)
		HAMILTONIO.SendCommands()

		LowestTimer = GetLowestTimer()
	
		Params = DESALT.GetAllDesaltParams()
		if LowestTimer["Wait Only"] == False:
			for key in Params:
				
				RemainingTime = LowestTimer["Wait Time"] - (time.time() - LowestTimer["Start Time"])
				#We want to calculte the remaining time each round so we do not accidently prevent an incubation ending

				if Params[key]["EQ Step"] == LowestTimer["Step"] and RemainingTime > Params[key]["Required EQ Time"] :
					DESALT.Equilibrate(key)
		#It is more efficient to equilibrate when the deck is not busy. So we will do it before we wait on a incubation timer

		RemainingTime = LowestTimer["Wait Time"] - (time.time() - LowestTimer["Start Time"])

		if RemainingTime > 0:
			HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Waiting for " + str(LowestTimer["Wait Reason"]) + ". Remaining wait time: " + str(int(RemainingTime/60) + 1) + ". Total wait time: " + str(int(LowestTimer["Wait Time"] / 60))}),False,True)
			HAMILTONIO.AddCommand(TIMER.Start({"WaitTime":RemainingTime}), not LowestTimer["Wait Only"])
			HAMILTONIO.AddCommand(TIMER.Wait({}), not LowestTimer["Wait Only"])
			HAMILTONIO.SendCommands()

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

			HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "A timer has expired during method progression. Starting follow-up."}),False,True)
			HAMILTONIO.SendCommands()

			if LowestTimer["Wait Only"] == False:
				STEPS.ActivateContext(LowestTimer["Step"].GetContext())

			LowestTimer["Callback"](LowestTimer["Step"])
			#Calls our callback function

def Callback(step):
	pass

def Step(step):

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Starting Pause Block. Block Coordinates: " + str(step.GetCoordinates())}),False,True)
	HAMILTONIO.SendCommands()

	Time = step.GetParameters()[TIME]

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []
	
	if type(Time) is str:
		MethodComments.append("The Time parameter can only be a number. Please Correct.")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)
		if HAMILTONIO.IsSimulated() == True:
			quit()
		else:
			STEPS.UpdateStepParams(step)
			Step(step)
			return

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Adding block to timer list to wait for " + str(Time) + " minutes"}),False,True)
	StartTimer(step, Time, Callback, "paused step")

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Ending Pause Block. Block Coordinates: " + str(step.GetCoordinates())}),False,True)
	HAMILTONIO.SendCommands()

