from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ..Labware import Plates as PLATES
from ...General import Log as LOG

TITLE = "Finish"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init():
	pass
		
def Step(step):
	LOG.BeginCommentsLog()

	PLATES.GetPlate(step.GetParentPlate()).Deactivate()

	LOG.Comment(str(step.GetParentPlate()) + " plate deactivated")

	LOG.EndCommentsLog()
	
	if len(PLATES.GetActivePlates()) == 0:
		WAIT.WaitForTimer()