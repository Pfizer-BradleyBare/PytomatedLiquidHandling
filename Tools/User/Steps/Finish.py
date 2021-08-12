from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ..Labware import Plates as PLATES


TITLE = "Finish"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init():
	pass
		
def Step(step):
	PLATES.GetPlate(step.GetParentPlate()).Deactivate()

	if len(PLATES.GetActivePlates()) == 0:
		WAIT.WaitForTimer()