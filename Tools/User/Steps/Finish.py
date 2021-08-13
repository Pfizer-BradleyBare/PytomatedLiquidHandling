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
	PLATES.GetPlate(step.GetParentPlate()).Deactivate()
	LOG.Step(step)
	LOG.GeneralComment(str(step.GetParentPlate()) + " plate deactivated")

	if len(PLATES.GetActivePlates()) == 0:
		WAIT.WaitForTimer()