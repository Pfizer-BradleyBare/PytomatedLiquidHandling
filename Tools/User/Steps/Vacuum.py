from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ...Hamilton.Commands import Transport as TRANSPORT
from ...Hamilton.Commands import Vacuum as VACUUM
from ...User import Configuration as CONFIGURATION

TITLE = "Vacuum"
SOURCE = "Source"
Volume = "Volume (uL)"
WAIT_TIME = "Pre Vacuum Wait (sec)"
PRESSURE = "Pressure Difference (mTorr)"
TIME = "Vacuum Time (sec)"

VacuumConfig = {}
TransportConfig = {}
IsUsedFlag = False

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def GetID():
	return VacuumConfig["COM_ID"]

def Init(MutableStepsList):
	global TransportConfig
	global VacuumConfig
	global IsUsedFlag

	VacuumConfig = CONFIGURATION.GetStepConfig(TITLE)
	TransportConfig = CONFIGURATION.GetStepConfig("Transport")

	CONFIGURATION.AddCheckSequence(VacuumConfig["Home"])
	CONFIGURATION.AddCheckSequence(VacuumConfig["Vacuum"])

	for item in VacuumConfig["PlateSequences"]:
		CONFIGURATION.AddCheckSequence(VacuumConfig["PlateSequences"][item])


	for Step in MutableStepsList:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			PLATES.GetPlate(Step.GetParentPlate()).SetVacuumState()


	
def Step(step):
	global VacuumConfig
	global TransportConfig

	Destination = step.GetParentPlate()
	SourcePlate = step.GetParameters()[SOURCE]
	Volume = step.GetParameters()[VOLUME]
	WaitTime = step.GetParameters()[WAIT_TIME]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	Loading = CONFIGURATION.GetDeckLoading(Destination)

	if Loading != None:


		Source = Loading["Sequence"]
		Destination = VacuumConfig["PlateSequences"][Loading["Labware Name"]]
		OpenWidth = TransportConfig[Loading["Labware Name"]]["Open"]
		CloseWidth = TransportConfig[Loading["Labware Name"]]["Close"]
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,0)
		#Move destination plate into vacuum

		Source = VacuumConfig["Home"]
		Destination = VacuumConfig["Vacuum"]
		OpenWidth = TransportConfig["Vacuum Manifold"]["Open"]
		CloseWidth = TransportConfig["Vacuum Manifold"]["Close"]
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,1)
		#Move manifold from park to vacuum

		step = LIQUID_TRANSFER.CreateStep(Destination,SourcePlate,SOLUTIONS.TYPE_REAGENT,SOLUTIONS.STORAGE_AMBIENT,Volume,Mix)
		LIQUID_TRANSFER.Step(step)
		#Transfer liquid into vacuum plate

		WAIT.StartTimer(step,WaitTime,WAIT.Callback())
		#Vacuum wait time

def Callback(step):
	global VacuumConfig
	global TransportConfig

	Destination = step.GetParentPlate()
	SourcePlate = step.GetParameters()[SOURCE]
	Volume = step.GetParameters()[VOLUME]
	WaitTime = step.GetParameters()[WAIT_TIME]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	Loading = CONFIGURATION.GetDeckLoading(Destination)

	if Loading != None:

		VACUUM.Start(Pressure, Time)
		VACUUM.Wait()
		#Start vacuum

		Destination = VacuumConfig["Home"]
		Source = VacuumConfig["Vacuum"]
		OpenWidth = TransportConfig["Vacuum Manifold"]["Open"]
		CloseWidth = TransportConfig["Vacuum Manifold"]["Close"]
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,1)
		#Move manifold from vacuum to park

		Destination = Loading["Sequence"]
		Source = VacuumConfig["PlateSequences"][Loading["Labware Name"]]
		OpenWidth = TransportConfig[Loading["Labware Name"]]["Open"]
		CloseWidth = TransportConfig[Loading["Labware Name"]]["Close"]
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,0)
		#Move destination plate back to loading position
