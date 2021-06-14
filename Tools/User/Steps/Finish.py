from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ..Labware import Plates as PLATES


TITLE = "Finish"

def Init():
	pass
		
def Step(step):
	PLATES.GetPlate(step.GetParentPlate()).Deactivate()

	if len(PLATES.GetActivePlates()) == 0:
		WAIT.WaitForTimer()