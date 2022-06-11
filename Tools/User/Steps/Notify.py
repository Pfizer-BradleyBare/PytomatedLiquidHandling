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

def DoesStatusUpdates():
	return True

def Init():
	pass

def Step(step):
	
	Parameters = step.GetParameters()
	Subject = Parameters[SUBJECT]
	Body = Parameters[MESSAGE]
	Wait = Parameters[WAIT_ON_USER]

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []
	
	#Testing subject and body?
	if not (type(Subject) is str):
		MethodComments.append("The Subject parameter must contain letters. Please Correct.")

	if not (type(Body) is str):
		MethodComments.append("The Body parameter must contain letters. Please Correct.")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(Step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	HAMILTONIO.AddCommand(NOTIFY.NotifyContacts({"Subject":Subject,"Body":Body,"Wait":Wait}))

	Response = HAMILTONIO.SendCommands()
	#No need to deal with response. Should always succeed