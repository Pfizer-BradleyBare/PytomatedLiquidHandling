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
		TestRun = True

	elif RunType == "Test":
		Initialization_Run = True
		GenerateList = False
		TestRun = True

else:
	Sample_Start_Pos = 1
	Excel_File_Path = "Method Maker.xlsm"
	Initialization_Run = True
	GenerateList = True
	TestRun = True

print("import")
import Tools.General.ExcelIO as EXCELIO
import Tools.General.HamiltonIO as HAMILTONIO
import Tools.General.Log as LOG

import Tools.User.Steps.Steps as STEPS
import Tools.User.Samples as SAMPLES
import Tools.User.Configuration as CONFIGURATION
import Tools.User.PrepList as PREPLIST
import Tools.User.Labware.Plates as PLATES
import Tools.User.Labware.Solutions as SOLUTIONS
import Tools.User.Labware.Labware as LABWARE

import Tools.User.Steps.Plate as PLATE
import Tools.User.Steps.Split_Plate as SPLIT_PLATE
import Tools.User.Steps.Merge_Plate as MERGE_PLATE
import Tools.User.Steps.Liquid_Transfer as LIQUID_TRANSFER
import Tools.User.Steps.Dilute as DILUTE
import Tools.User.Steps.Desalt as DESALT
import Tools.User.Steps.Wait as WAIT
import Tools.User.Steps.Incubate as INCUBATE
import Tools.User.Steps.Vacuum as VACUUM
import Tools.User.Steps.Notify as NOTIFY
import Tools.User.Steps.Finish as FINISH
import Tools.User.Steps.Aliquot as ALIQUOT
import Tools.User.Steps.Pool as POOL
import Tools.User.Steps.PreLoad_Liquid as PRELOAD_LIQUID
import Tools.User.Steps.MagneticBeads as MAGNETIC_BEADS
import Tools.User.Steps.Merge_Plate as MERGE_PLATE

import Tools.Hamilton.PreRun as PRERUN
##import Tools.Hamilton.Commands.StatusUpdate as STATUS_UPDATE

try:

	print("Init Classes")
	EXCELIO.Init(Excel_File_Path)
	HAMILTONIO.Init()
	HAMILTONIO.Simulated(Initialization_Run)
	if TestRun == True:
		LOG.Init("Test Log",True)
	else:
		LOG.Init("Run Log",True)
	#init IOs

	#
	# The first thing I want to do is check that the method is validated. If it is not then we will exit and inform the user.
	#
	ValidatedStatus = EXCELIO.GetMethodValidatedStatus()
	#if  ValidatedStatus == "Blocks":
	#	EXCELIO.CreateCriticalMessageBox("There is a validation issue with the Building Blocks. Please close and reopen the workbook to fix. If that doesn't work, please contact a Hamilton SME.", "Blocks Validation Failed")
	#	quit()
	#elif ValidatedStatus == "Actions":
	#	EXCELIO.CreateCriticalMessageBox("There is a validation issue with the method. Please check the method sheet for red cells and correct it.", "Method Validation Failed")
	#	quit()
	#elif ValidatedStatus == "Solutions":
	#	EXCELIO.CreateCriticalMessageBox("There is a validation issue with the Solutions. Please check the Solutions sheet for red cells and correct it.", "Solutions Validation Failed")
	#	quit()

	CONFIGURATION.Init()
	PREPLIST.Init()
	STEPS.Init(EXCELIO.GetMethod())
	SAMPLES.Init(Sample_Start_Pos, EXCELIO.GetWorklist())
	LABWARE.Init()
	#Init Trackers


	PLATE.Init(STEPS.GetSteps())
	SPLIT_PLATE.Init(STEPS.GetSteps())
	MERGE_PLATE.Init(STEPS.GetSteps())
	LIQUID_TRANSFER.Init()
	DILUTE.Init()
	DESALT.Init(STEPS.GetSteps())
	WAIT.Init()
	INCUBATE.Init(STEPS.GetSteps())
	NOTIFY.Init()
	FINISH.Init()
	ALIQUOT.Init(STEPS.GetSteps())
	POOL.Init(STEPS.GetSteps())
	PRELOAD_LIQUID.Init(STEPS.GetSteps())
	VACUUM.Init(STEPS.GetSteps())
	MAGNETIC_BEADS.Init(STEPS.GetSteps())
	MERGE_PLATE.Init(STEPS.GetSteps())



	#init steps
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

		FINISH.TITLE: FINISH.Step,

		ALIQUOT.TITLE: ALIQUOT.Step,

		POOL.TITLE: POOL.Step,

		PRELOAD_LIQUID.TITLE: PRELOAD_LIQUID.Step,

		MAGNETIC_BEADS.TITLE: MAGNETIC_BEADS.Step,

		MERGE_PLATE.TITLE: MERGE_PLATE.Step,

		WAIT.TITLE: WAIT.Step
	}

	while(True):

		WAIT.CheckForExpiredTimers()
		#Wait is async, but we need to ensure that we are not continuously pausing a context that is ready to continue running.

		Step = STEPS.GetNextStep()

		if Step == None:
			break

		if sum(LABWARE.GetContextualFactors(STEPS.Class.GetContext(Step))) == 0 and Step.GetTitle() != MERGE_PLATE.TITLE:
			continue
		#We also want to ensure that the parent is actually used. To do this, we can sum the parent plate factors. 
		# If it is 0 then the plate is not used by any samples.
		#We do not want to skip a merge plates step no matter what.

		STEPS.UpdateStepParams(Step)
		PLATES.LABWARE.GetExcelLabwareInfo()
		#This updates the actual step parameters at time the step is run. This allows for method development in real time

		print("\n",Step)

		LOG.LogStep(Step)
		LOG.PublishLog()

		Steps[Step.GetTitle()](Step)
		#This does the step

	#do each step

	print("\n\n\n\n")

	if HAMILTONIO.IsSimulated() == True:

		if GenerateList == False and TestRun == False:
			HAMILTONIO.Simulated(False)

		HAMILTONIO.AddCommand(PRERUN.Samples(SAMPLES.GetNumSamples()),False)
		Labware = CONFIGURATION.Load(LABWARE.GetAllLabwareType(LABWARE.LabwareTypes.Plate),LABWARE.GetAllLabwareType(LABWARE.LabwareTypes.Reagent))
		HAMILTONIO.AddCommand(PRERUN.Labware(Labware),False)

		PREPLIST.PrintFinalPlateVolumes(Labware)

		if GenerateList == True:
			PREPLIST.GeneratePrepSheet(Labware)
		#Generate prep sheet here
		
		if LIQUID_TRANSFER.IsUsed() == True or DILUTE.IsUsed() == True:
			HAMILTONIO.AddCommand(PRERUN.PIPETTE.PreRun(PLATES.GetAllPipetteVolumes()),False)
		
		if INCUBATE.IsUsed() == True:
			HAMILTONIO.AddCommand(PRERUN.HEATER.PreRun({}),False)
		
		if NOTIFY.IsUsed() == True:
			HAMILTONIO.AddCommand(PRERUN.NOTIFY.PreRun({}),False)
		
		if DESALT.IsUsed() == True:
			HAMILTONIO.AddCommand(PRERUN.DESALT.PreRun(DESALT.GetDesaltParams()),False)

		if WAIT.IsUsed() == True:
			HAMILTONIO.AddCommand(PRERUN.TIMER.PreRun({}),False)

		if INCUBATE.IsUsed() == True or VACUUM.IsUsed() == True:
			HAMILTONIO.AddCommand(PRERUN.TRANSPORT.PreRun({}),False)

		if VACUUM.IsUsed() == True:
			HAMILTONIO.AddCommand(PRERUN.VACUUM.PreRun({"VacuumPlateNames":VACUUM.GetVacPlates()}),False)

		if MAGNETIC_BEADS.IsUsed() == True:
			HAMILTONIO.AddCommand(PRERUN.MAGNETIC_BEADS.PreRun({"PlateNames":MAGNETIC_BEADS.GetUsedParentPlateNames()}),False)

		##if STATUS_UPDATE.IsUsed() == True:
		HAMILTONIO.AddCommand(PRERUN.STATUS_UPDATE.PreRun({}),False)
		HAMILTONIO.AddCommand(PRERUN.LID.PreRun({}),False)
					

		Response = HAMILTONIO.SendCommands()

		#if LOG.Exists() and TestRun == False and len(LOG.GetLatestStep()) != 0:
		#	HAMILTONIO.AddCommand(PRERUN.LOG.PreRun(LOG.GetLatestStep()),False)
		#	Response = HAMILTONIO.SendCommands()
		#	LOG.HandleResponse(Response[0])
		#initialize all the Hamilton Libraries.


	HAMILTONIO.EndCommunication()

	if TestRun == True:
		if GenerateList == True:
			EXCELIO.SelectCell("Preparation List",1,1)
			EXCELIO.CreateInformationMessageBox("Preperation sheet generation completed succesfully!", "Successful Execution")
		else:
			EXCELIO.CreateInformationMessageBox("Method test completed succesfully! Please see the Test Log and Final Plate Volumes sheet to confirm the method performed as expected.", "Successful Execution")
except Exception as e:
	EXCELIO.CreateCriticalMessageBox("An undefined error has occured. Unfortunately, this error is not captured by the normal error handling. Please contact a Hamilton SME to correct the issue.","Undefined Error Occured")