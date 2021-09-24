from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ..Steps import Liquid_Transfer as LIQUID_TRANSFER
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...Hamilton.Commands import Transport as TRANSPORT
from ...Hamilton.Commands import Vacuum as VACUUM
from ...User import Configuration as CONFIGURATION
from ...General import Log as LOG

TITLE = "Vacuum"
SOURCE = "Source"
VOLUME = "Volume (uL)"
VACUUM_PLATE = "Vacuum Plate"
WAIT_TIME = "Pre Vacuum Wait (min)"
PRESSURE = "Pressure Difference (mTorr)"
TIME = "Vacuum Time (min)"

VacuumConfig = {}
TransportConfig = {}
IsUsedFlag = False
VacuumPlate = None

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def GetVacuumParams():
	global VacuumConfig
	global VacuumPlate
	return {"ID":VacuumConfig["COM_ID"], "Plate":VacuumPlate}


def Init(MutableStepsList, SequencesList):
	global TransportConfig
	global VacuumConfig
	global IsUsedFlag
	global VacuumPlate

	VacuumConfig = CONFIGURATION.GetStepConfig(TITLE)
	TransportConfig = CONFIGURATION.GetStepConfig("Transport")

	CONFIGURATION.AddCheckSequence(VacuumConfig["Home"])
	CONFIGURATION.AddCheckSequence(VacuumConfig["Vacuum"])

	for item in VacuumConfig["PlateSequences"]:
		CONFIGURATION.AddCheckSequence(VacuumConfig["PlateSequences"][item])

	for item in VacuumConfig["VacuumPlates"]:
		CONFIGURATION.AddCheckSequence(VacuumConfig["VacuumPlates"][item]["Sequence"])

	VacPlates = set()

	for Step in MutableStepsList:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			PLATES.AddPlate(VacuumConfig["VacuumPlates"][Step.GetParameters()[VACUUM_PLATE]]["Sequence"], "Vacuum", SequencesList)
			CONFIGURATION.AddOmitLoading(VacuumConfig["VacuumPlates"][Step.GetParameters()[VACUUM_PLATE]]["Sequence"])
			PLATES.GetPlate(Step.GetParentPlate()).SetVacuumState()
			VacPlates.add(Step.GetParameters()[VACUUM_PLATE])

	if len(VacPlates) > 1:
		print("Only one vacuum plate is supported at this time")
		quit()
	elif len(VacPlates) == 1:
			VacuumPlate = list(VacPlates)[0]


	
def Step(step):
	global VacuumConfig
	global TransportConfig

	Destination = step.GetParentPlate()
	SourcePlate = step.GetParameters()[SOURCE]
	Volume = step.GetParameters()[VOLUME]
	WaitTime = step.GetParameters()[WAIT_TIME]
	VacPlate = step.GetParameters()[VACUUM_PLATE]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	Plate = VacuumConfig["VacuumPlates"][VacPlate]["Sequence"]

	Loading = CONFIGURATION.GetDeckLoading(Destination)

	if Loading != None:

		Source = Loading["Sequence"]
		Destination = VacuumConfig["PlateSequences"][Loading["Labware Name"]]
		OpenWidth = TransportConfig[Loading["Labware Name"]]["Open"]
		CloseWidth = TransportConfig[Loading["Labware Name"]]["Close"]
		LOG.BeginCommandLog()
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,0,0)
		LOG.EndCommandLog()
		#Move destination plate into vacuum

		Source = VacuumConfig["Home"]
		Destination = VacuumConfig["Vacuum"]
		OpenWidth = TransportConfig["Vacuum Manifold"]["Open"]
		CloseWidth = TransportConfig["Vacuum Manifold"]["Close"]
		LOG.BeginCommandLog()
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,1,0)
		LOG.EndCommandLog()
		#Move manifold from park to vacuum

	LTstep = LIQUID_TRANSFER.CreateStep(Plate,SourcePlate,SOLUTIONS.TYPE_REAGENT,SOLUTIONS.STORAGE_AMBIENT,Volume,"N/A")
	LIQUID_TRANSFER.Step(LTstep)
	#Transfer liquid into vacuum plate

	WAIT.StartTimer(step,WaitTime,Callback)
	#Vacuum wait time

def Callback(step):
	global VacuumConfig
	global TransportConfig

	Destination = step.GetParentPlate()
	Volume = step.GetParameters()[VOLUME]
	VacPlate = step.GetParameters()[VACUUM_PLATE]
	WaitTime = step.GetParameters()[WAIT_TIME]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]
	Plate = VacuumConfig["VacuumPlates"][VacPlate]["Sequence"]

	Loading = CONFIGURATION.GetDeckLoading(Destination)

	try:
		TruePressure = VacuumConfig["VacuumPlates"][VacPlate]["Pressures"][Pressure]
	except:
		TruePressure = Pressure

	PLATES.GetPlate(Destination).CreatePipetteSequence(SAMPLES.Column(Plate), SAMPLES.Column(Volume),SAMPLES.Column("N/A"))

	LOG.BeginCommandLog()
	VACUUM.Start(TruePressure, Time*60)
	LOG.EndCommandLog()
	#Start vacuum

	if Loading != None:

		Destination = VacuumConfig["Home"]
		Source = VacuumConfig["Vacuum"]
		OpenWidth = TransportConfig["Vacuum Manifold"]["Open"]
		CloseWidth = TransportConfig["Vacuum Manifold"]["Close"]
		LOG.BeginCommandLog()
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,0,0)
		LOG.EndCommandLog()
		#Move manifold from vacuum to park

		Destination = Loading["Sequence"]
		Source = VacuumConfig["PlateSequences"][Loading["Labware Name"]]
		OpenWidth = TransportConfig[Loading["Labware Name"]]["Open"]
		CloseWidth = TransportConfig[Loading["Labware Name"]]["Close"]
		LOG.BeginCommandLog()
		TRANSPORT.Move(Source,Destination,OpenWidth,CloseWidth,1,1)
		LOG.EndCommandLog()
		#Move destination plate back to loading position
