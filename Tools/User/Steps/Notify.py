from ..Steps import Steps as STEPS
from ...Hamilton.Commands import Notify as NOTIFY
from ...General import Log as LOG
from ...General import HamiltonIO as HAMILTONIO

TITLE = "Notify"
WAIT_ON_USER = "Wait On User"
SUBJECT = "Subject"
MESSAGE = "Message"

IsUsedFlag = True

def IsUsed():
	return IsUsedFlag

def Init():
	pass

def Step(step):
	
	Parameters = step.GetParameters()

	HAMILTONIO.AddCommand(NOTIFY.NotifyContacts({"Subject":Parameters[SUBJECT],"Body":Parameters[MESSAGE],"Wait":Parameters[WAIT_ON_USER]}))

	Response = HAMILTONIO.SendCommands()
	#No need to deal with response. Should always succeed