
import os
import time
from ..General import Log as LOG

BaseFolder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
Folder = "CommunicationFolder"
HAMILTON_COMMAND_FILE = os.path.join(BaseFolder, Folder,"Command.txt")
HAMILTON_COMMAND_TEMP_FILE = os.path.join(BaseFolder, Folder,"Temp_Command.txt")
HAMILTON_RESPONSE_TEMP_FILE = os.path.join(BaseFolder, Folder,"Temp_Response.txt")
HAMILTON_RESPONSE_FILE = os.path.join(BaseFolder, Folder,"Response.txt")

COMMAND_DELIMITER = ";;;"

def GetDelimiter():
	global COMMAND_DELIMITER
	return COMMAND_DELIMITER

SimulatedIO = None

######################################################################### 
#	Description: Initializes the HamiltonIO system in the simulated state
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Init():
	global SimulatedIO
	SimulatedIO = True

######################################################################### 
#	Description: Changes the state of the Hamilton IO. True indicates the Hamilton response is simulated
#	Input Arguments: [Simulate: True or False]
#	Returns: N/A
#########################################################################
def Simulated(Simulate):
	global SimulatedIO
	SimulatedIO = Simulate


def IsSimulated():
	global SimulatedIO
	return SimulatedIO

CommandsList = []
def AddCommand(CommandString, Log=True):
	global CommandsList

	LOG.BeginCommandLog()

	if LOG.CommandInLog(CommandString) != True:
		LOG.Command(CommandString)
		CommandsList.append(CommandString)
		if Log == True:
			LOG.CommandID()

	LOG.EndCommandLog()

######################################################################### 
#	Description: Pushes a command to the communication channel for the Hamilton.
#	The first file creates is a temporary file. As soon as write is complete the file is renamed to a file the Hamilton expects.
#	Input Arguments: [Command: String]
#	Returns: N/A
#########################################################################
def SendCommands():
	global CommandsList
	
	#Create the command list to send
	Command = ""
	for CommandString in CommandsList:
		Command = Command + CommandString + "\n"

	#Reset CommandsList
	CommandsList = []

	#Send the command list
	global SimulatedIO
	if SimulatedIO == False and Command != "":
		file = open(HAMILTON_COMMAND_TEMP_FILE, "w")
		file.write(Command)
		file.close()
		os.rename(HAMILTON_COMMAND_TEMP_FILE, HAMILTON_COMMAND_FILE)

		#Wait for Hamilton Response
		while os.path.exists(HAMILTON_RESPONSE_FILE) == False:
			time.sleep(0.1)

		#Wait a little longer so Hamilton will release it.
		time.sleep(0.1)

		#Read it and evaluate into an array of dictionaries
		file = open(HAMILTON_RESPONSE_FILE, "r")
		Response = file.read()
		print(Response)
		Response = eval(Response)
		file.close()
		os.remove(HAMILTON_RESPONSE_FILE)
		
		if Response == []:
			file = open(HAMILTON_COMMAND_TEMP_FILE, "w")
			file.write("END")
			file.close()
			os.rename(HAMILTON_COMMAND_TEMP_FILE, HAMILTON_COMMAND_FILE)
			quit()
		return Response
	return False

######################################################################### 
#	Description: Pushes a command to the communication channel for the Hamilton.
#	The first file creates is a temporary file. As soon as write is complete the file is renamed to a file the Hamilton expects.
#	Input Arguments: [Command: String]
#	Returns: N/A
#########################################################################
def Push(Command):
	pass

######################################################################### 
#	Description: Reads a response from the Hamilton. As soon as the response is read the file is deleted.
#	Input Arguments: N/A
#	Returns: [String]
#########################################################################
def Pull():
	pass



######################################################################### 
#	Description: Ends the communication on the Hamilton system
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def EndCommunication():
	AddCommand("END",False)
	SendCommands()
