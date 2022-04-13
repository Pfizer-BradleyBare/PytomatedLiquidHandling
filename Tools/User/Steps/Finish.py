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

	STEPS.DeactivateContext(step.GetContext())

	LOG.Comment(str(step.GetParentPlate()) + " plate deactivated")

	LOG.EndCommentsLog()
	
	if len(STEPS.GetActiveContexts()) == 0:
		WAIT.WaitForTimer()