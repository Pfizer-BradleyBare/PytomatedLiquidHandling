from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Steps import Split_Plate as SPLIT_PLATE
from ...General import Log as LOG

TITLE = "Pool"
NAME = "Name"
TYPE = "Type"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	pass

def Step(step):
	LOG.BeginCommentsLog()
	LOG.EndCommentsLog()
	pass