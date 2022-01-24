from ..Steps import Steps as STEPS
from ...Hamilton.Commands import Notify as NOTIFY
from ...General import Log as LOG

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
	LOG.BeginCommentsLog()
	
	Parameters = step.GetParameters()

	LOG.EndCommentsLog()

	NOTIFY.NotifyContacts({"Subject":Parameters[SUBJECT],"Body":Parameters[MESSAGE],"Wait":Parameters[WAIT_ON_USER]})
