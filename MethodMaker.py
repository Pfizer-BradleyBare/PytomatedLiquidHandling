import sys
import time

if len(sys.argv) > 1:
	Excel_File_Path = sys.argv[1]
	Sample_Start_Pos = int(sys.argv[2])
	RunType = sys.argv[3]

	if RunType == "Run":
		Initialization_Run = False
		GenerateList = False
		TestRun = False

	elif RunType == "Init":
		Initialization_Run = True
		GenerateList = False
		TestRun = False

	elif RunType == "PrepList":
		Initialization_Run = True
		GenerateList = True
		TestRun = False

	elif RunType == "Test":
		Initialization_Run = True
		GenerateList = False
		TestRun = True

else:
	Sample_Start_Pos = 1
	Excel_File_Path = "Method Maker2.xlsm"
	Initialization_Run = True
	GenerateList = True
	TestRun = True

print("import")
import Tools.General.ExcelIO as EXCELIO
import Tools.General.HamiltonIO as HAMILTONIO

import Tools.User.Steps.Steps as STEPS
import Tools.User.Samples as SAMPLES
import Tools.User.Configuration as CONFIGURATION
import Tools.User.Labware.Plates as PLATES
import Tools.User.Labware.Solutions as SOLUTIONS

import Tools.User.Steps.Plate as PLATE
import Tools.User.Steps.Split_Plate as SPLIT_PLATE
import Tools.User.Steps.Liquid_Transfer as LIQUID_TRANSFER
import Tools.User.Steps.Dilute as DILUTE
import Tools.User.Steps.Desalt as DESALT
import Tools.User.Steps.Wait as WAIT
import Tools.User.Steps.Incubate as INCUBATE
import Tools.User.Steps.Vacuum as VACUUM
import Tools.User.Steps.Notify as NOTIFY
import Tools.User.Steps.Finish as FINISH

import Tools.Hamilton.PreRun as PRERUN

print("Init Classes")
EXCELIO.Init(Excel_File_Path)
HAMILTONIO.Init()
HAMILTONIO.Simulated(Initialization_Run)
#init IOs

CONFIGURATION.Init()
STEPS.Init(EXCELIO.GetMethod())
SAMPLES.Init(Sample_Start_Pos, EXCELIO.GetWorklist())
PLATES.Init()
SOLUTIONS.Init()
#Init Trackers

PLATE.Init(STEPS.GetSteps(), SAMPLES.GetSequences())
SPLIT_PLATE.Init(STEPS.GetSteps())
LIQUID_TRANSFER.Init()
DILUTE.Init()
DESALT.Init(STEPS.GetSteps())
WAIT.Init()
INCUBATE.Init(STEPS.GetSteps())
NOTIFY.Init()
FINISH.Init()
#init steps

PLATES.StartStepSequence(STEPS.GetStartingPlate())
STEPS.StartStepSequence()

Steps = {
	PLATE.TITLE: PLATE.Step,

	SPLIT_PLATE.TITLE: SPLIT_PLATE.Step,

	LIQUID_TRANSFER.TITLE: LIQUID_TRANSFER.Step,

	DILUTE.TITLE: DILUTE.Step,

	DESALT.TITLE: DESALT.Step,

	INCUBATE.TITLE: INCUBATE.Step,

	VACUUM.TITLE: VACUUM.Step,

	NOTIFY.TITLE: NOTIFY.Step,

	FINISH.TITLE: FINISH.Step
}

while(True):
	Step = STEPS.GetNextStep(PLATES.GetActivePlates())

	if Step == None:
		break

	print("\n", Step)
	Steps[Step.GetTitle()](Step)
#do each step

if HAMILTONIO.IsSimulated() == True:

	if GenerateList == False and TestRun == False:
		HAMILTONIO.Simulated(False)

	PRERUN.Samples(SAMPLES.GetTotalSamples())
	Labware = CONFIGURATION.Load(PLATES.GetPlates(),SOLUTIONS.GetSolutions())
	PRERUN.CheckSequences(CONFIGURATION.GetCheckSequences())
	PRERUN.Labware(Labware)

	CONFIGURATION.WriteLoadingInformation(Labware)

	if GenerateList == True:
		pass
		CONFIGURATION.GeneratePrepSheet(Labware)
	#Generate prep sheet here
	
	if LIQUID_TRANSFER.IsUsed() == True or DILUTE.IsUsed() == True:
		PRERUN.PIPETTE.PreRun(SOLUTIONS.GetPipetteVolumes())
	
	if INCUBATE.IsUsed() == True:
		PRERUN.HEATER.PreRun(INCUBATE.GetHeaterList())
	
	if NOTIFY.IsUsed() == True:
		PRERUN.NOTIFY.PreRun()
	
	if DESALT.IsUsed() == True:
		PRERUN.DESALT.PreRun(DESALT.GetDesaltParams())

	if WAIT.IsUsed() == True:
		PRERUN.TIMER.PreRun()

	if INCUBATE.IsUsed() == True:
		PRERUN.TRANSPORT.PreRun()
	#initialize all the Hamilton Libraries.


HAMILTONIO.EndCommunication()