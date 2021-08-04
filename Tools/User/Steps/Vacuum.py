from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Transport as TRANSPORT
from ...Hamilton.Commands import Vacuum as VACUUM
from ...User import Configuration as CONFIGURATION

TITLE = "Vacuum"
SOURCE = "Source Plate"
PRESSURE = "Pressure Difference (mTorr)"
TIME = "Time (sec)"

VacuumConfig = {}
TransportConfig = {}
IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init(MutableStepsList):
	global TransportConfig
	global VacuumConfig

	VacuumConfig = CONFIGURATION.GetStepConfig(TITLE)
	TransportConfig = CONFIGURATION.GetStepConfig("Transport")
	
def Step(step):
	global VacuumConfig
	global TransportConfig

	Destination = step.GetParentPlate()
	SourcePlate = step.GetParameters()[SOURCE]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	Loading = CONFIGURATION.GetDeckLoading(Destination)

	PLATES.GetPlate(Destination).CreatePipetteSequence(SAMPLES.Column(SourcePlate),PLATES.GetPlate(SourcePlate).GetVolumesList())

	if Loading != None:

		Source = Loading["Sequence"]
		Destination = VacuumConfig["Plate Sequences"][Loading["Labware Type"]][Loading["Max Volume"]]
		OpenWidth = TransportConfig[Loading["Labware Type"]][Loading["Max Volume"]]["Open"]
		CloseWidth = TransportConfig[Loading["Labware Type"]][Loading["Max Volume"]]["Close"]
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,0)

		Source = VacuumConfig["Vacuum Sequences"]["Home"]
		Destination = VacuumConfig["Vacuum Sequences"]["Vacuum"]
		OpenWidth = TransportConfig["Vacuum"]["Open"]
		CloseWidth = TransportConfig["Vacuum"]["Close"]
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,1)

		VACUUM.Start(Pressure, Time)
		#Start Vacuum
		VACUUM.Wait()
		#Wait

		Destination = VacuumConfig["Vacuum Sequences"]["Home"]
		Source = VacuumConfig["Vacuum Sequences"]["Vacuum"]
		OpenWidth = TransportConfig["Vacuum"]["Open"]
		CloseWidth = TransportConfig["Vacuum"]["Close"]
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,0)

		Destination = Loading["Sequence"]
		Source = VacuumConfig["Plate Sequences"][Loading["Labware Type"]][Loading["Max Volume"]]
		OpenWidth = TransportConfig[Loading["Labware Type"]][Loading["Max Volume"]]["Open"]
		CloseWidth = TransportConfig[Loading["Labware Type"]][Loading["Max Volume"]]["Close"]
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,1)
		#Remove
		#Remove



