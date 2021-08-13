from ..User.Labware import Plates as PLATES
from ..User.Labware import Solutions as SOLUTIONS
from ..User import Configuration as CONFIGURATION
from ..General import ExcelIO as EXCELIO
from ..General import HamiltonIO as HAMILTONIO
from ..User import Samples as SAMPLES
import copy
import yaml
import os
import os.path
import collections

######################################################################### 
#	Description: Initializes the library by pulling information from Config files
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Init():
	pass


def NumericToAlphaNumeric(Number):
	Alpha = int((Number-1) / 8)
	Numeric = Number % 8
	if Numeric == 0:
		Numeric = 8
	AN = str(chr(65+Alpha)) + str(Numeric)
	return AN


def GeneratePrepSheet(LabwareArray):
	StartRow = 2
	StartCol = 2
	MaxCol = 11
	CurrentRow = StartRow
	CurrentCol = StartCol
	RowPadding = 2
	ColPadding = 2
	RowTracker = 0

	try:
		EXCELIO.DeleteSheet("PrepList")
	except:
		pass

	EXCELIO.CreateSheet("PrepList")

	for Labware in LabwareArray:
		IsPlate = PLATES.IsPlate(Labware)

		if IsPlate == True and PLATES.GetPlate(Labware).LoadingRequired():
			Plate = PLATES.GetPlate(Labware)
			LoadingDict = CONFIGURATION.GetDeckLoading(Labware)

			if LoadingDict != None:
				DeadVolumeConfig = CONFIGURATION.GetSysConfig()["Dead Volume"]

				PlatePrepArray = dict()
				for index in range(0,SAMPLES.GetNumSamples()):
					for position in Plate.GetSequenceList()[index]:
						if Plate.GetVolumesList()[index] != 0:
							if int(position) in PlatePrepArray:
								PlatePrepArray[int(position)]["Volume"] += abs(Plate.GetVolumesList()[index])
							else:
								PlatePrepArray[int(position)] = {"AlphaNumeric":NumericToAlphaNumeric(position),"Volume":abs(Plate.GetVolumesList()[index]) + DeadVolumeConfig[LoadingDict["Labware Name"]]}

				#PlatePrepArray = sorted(PlatePrepArray, key=lambda x: x["Position"])
				
				UsedSpace = EXCELIO.PrintPlate(CurrentRow, CurrentCol, Plate.GetName(), LoadingDict["Labware Name"], 8, 12, PlatePrepArray)

				NewRow = UsedSpace[0] + CurrentRow
				NewCol = UsedSpace[1] + CurrentCol
				
				if NewRow > RowTracker:
					RowTracker = NewRow

				if NewCol > MaxCol:
					CurrentCol = StartCol
					CurrentRow = RowTracker + RowPadding
				else:
					CurrentCol = NewCol + ColPadding
			#Do plate solution sheet here


	CurrentRow = RowTracker + RowPadding * 2
	CurrentCol = StartCol

	for Labware in LabwareArray:
		IsPlate = PLATES.IsPlate(Labware)
		if IsPlate == False:
			LoadingDict = CONFIGURATION.GetDeckLoading(Labware)

			if LoadingDict != None:

				UsedSpace = EXCELIO.PrintReagent(CurrentRow, CurrentCol, Labware, LoadingDict["Labware Name"], LoadingDict["Volume"])

				NewRow = UsedSpace[0] + CurrentRow
				NewCol = UsedSpace[1] + CurrentCol
				
				if NewRow > RowTracker:
					RowTracker = NewRow

				if NewCol > MaxCol:
					CurrentCol = StartCol
					CurrentRow = RowTracker + RowPadding
				else:
					CurrentCol = NewCol + ColPadding
			#Do reagent solution loading here

	EXCELIO.AutoFit("PrepList")	





