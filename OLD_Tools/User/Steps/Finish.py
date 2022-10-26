from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ..Labware import Plates as PLATES
from ...General import Log as LOG

TITLE = "Finish"

IsUsedFlag = True

def IsUsed():
	return IsUsedFlag

def DoesStatusUpdates():
	return False

def Init():
	pass
		
def Step(step):

	STEPS.DeactivateContext(step.GetContext())
	
	if STEPS.GetNumActiveContexts() == 0:
		WAIT.WaitForTimer()