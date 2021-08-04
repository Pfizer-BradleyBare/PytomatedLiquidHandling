from ..Steps import Steps as STEPS
from ...Hamilton.Commands import Notify as NOTIFY

TITLE = "Notify"
WAIT_ON_USER = "Wait On User"
SUBJECT = "Subject"
MESSAGE = "Message"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init():
	pass

def Step(step):
	Parameters = step.GetParameters()
	NOTIFY.SendMessage(Parameters[WAIT_ON_USER],Parameters[SUBJECT],Parameters[MESSAGE])