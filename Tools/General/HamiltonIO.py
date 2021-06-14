
import os
import time

BaseFolder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
Folder = "CommunicationFolder"
HAMILTON_COMMAND_FILE = os.path.join(BaseFolder, Folder,"Command.txt")
HAMILTON_COMMAND_TEMP_FILE = os.path.join(BaseFolder, Folder,"Temp_Command.txt")
HAMILTON_RESPONSE_TEMP_FILE = os.path.join(BaseFolder, Folder,"Temp_Response.txt")
HAMILTON_RESPONSE_FILE = os.path.join(BaseFolder, Folder,"Response.txt")

SimulatedIO = None

def Init():
	global SimulatedIO
	SimulatedIO = True

def Simulated(Simulate):
	global SimulatedIO
	SimulatedIO = Simulate

def Push(Command):
	global SimulatedIO
	if SimulatedIO == False:
		file = open(HAMILTON_COMMAND_TEMP_FILE, "w")
		file.write(Command)
		file.close()
		os.rename(HAMILTON_COMMAND_TEMP_FILE, HAMILTON_COMMAND_FILE)

def Pull():
	global SimulatedIO
	if SimulatedIO == False:
		while os.path.exists(HAMILTON_RESPONSE_FILE) == False:
			time.sleep(0.1)

		file = open(HAMILTON_RESPONSE_FILE, "r")
		Response = file.read()
		file.close()
		time.sleep(0.1)
		os.remove(HAMILTON_RESPONSE_FILE)
		if Response == "Abort":
			Push("END")
			quit()
		return Response

def EndCommunication():
	Push("END")
	Pull()