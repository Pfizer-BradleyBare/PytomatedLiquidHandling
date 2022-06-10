from ..User.Labware import Labware as LABWARE
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
	Sheet = "Preparation List"
	StartRow = 2
	StartCol = 2
	MaxCol = 11
	CurrentRow = StartRow
	CurrentCol = StartCol
	RowPadding = 2
	ColPadding = 2
	RowTracker = 0

	try:
		EXCELIO.DeleteSheet(Sheet)
	except:
		pass

	EXCELIO.CreateSheet(Sheet)

	for LabwareName in LabwareArray:
		Labware = LABWARE.GetLabware(LabwareName)

		if Labware.GetLabwareType() == LABWARE.LabwareTypes.Plate:
			PlateLoadedVolumeList = Labware.MinVolumeList
			if True:

				PlatePrepArray = dict()
				for index in range(0,SAMPLES.GetNumSamples()):
						position = index + 1
					#for position in Plate.GetSequences()[index]:
						if PlateLoadedVolumeList[index] != 0:
							if Labware.GetIsPreloaded() == True:
								PlatePrepArray[int(position)] = {"AlphaNumeric":position,"Volume":"{:.2f}".format(abs(PlateLoadedVolumeList[index]))}
							else:
								PlatePrepArray[int(position)] = {"AlphaNumeric":position,"Volume":"{:.2f}".format(abs(PlateLoadedVolumeList[index]) + LabwareArray[LabwareName]["Labware Info"]["Dead Volume"])}
				
				if len(PlatePrepArray) != 0:
					UsedSpace = EXCELIO.PrintPlate(Sheet, CurrentRow, CurrentCol, LabwareName, LabwareArray[LabwareName]["Labware Name"], LabwareArray[LabwareName]["Labware Info"]["Labware Rows"], LabwareArray[LabwareName]["Labware Info"]["Labware Columns"], PlatePrepArray)

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

	for LabwareName in LabwareArray:
		Labware = LABWARE.GetLabware(LabwareName)

		if Labware.GetLabwareType() == LABWARE.LabwareTypes.Reagent:
			if Labware.GetMaxVolume() != 0:

				UsedSpace = EXCELIO.PrintReagent(Sheet, CurrentRow, CurrentCol, LabwareName, LabwareArray[LabwareName]["Labware Name"], "{:.2f}".format(LabwareArray[LabwareName]["Used Volume"]))

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

	for Column in range(1,50):
		EXCELIO.AutoFit(Sheet,Column)	


def PrintFinalPlateVolumes(LabwareArray):
	Sheet = "Final Plate Volumes"
	StartRow = 6
	StartCol = 2
	MaxCol = 11
	CurrentRow = StartRow
	CurrentCol = StartCol
	RowPadding = 2
	ColPadding = 2
	RowTracker = 0

	try:
		EXCELIO.DeleteSheet(Sheet)
	except:
		pass

	EXCELIO.CreateSheet(Sheet)

	TrackedMaxCol = StartCol + MaxCol - 1

	for LabwareName in LabwareArray:
		Labware = LABWARE.GetLabware(LabwareName)

		if Labware.GetLabwareType() == LABWARE.LabwareTypes.Plate:

			PlatePrepArray = dict()
			for index in range(0,SAMPLES.GetNumSamples()):
				
				position = index + 1
				
				if Labware.VolumesList[index] > 0:
					PlatePrepArray[int(position)] = {"AlphaNumeric":index + 1,"Volume":"{:.2f}".format(Labware.VolumesList[index])}
			
			if len(PlatePrepArray) != 0:

				UsedSpace = EXCELIO.PrintPlate(Sheet, CurrentRow, CurrentCol, LabwareName, LabwareArray[LabwareName]["Labware Name"], LabwareArray[LabwareName]["Labware Info"]["Labware Rows"], LabwareArray[LabwareName]["Labware Info"]["Labware Columns"], PlatePrepArray)

				NewRow = UsedSpace[0] + CurrentRow
				NewCol = UsedSpace[1] + CurrentCol
			
				if NewCol > TrackedMaxCol:
					TrackedMaxCol = NewCol - 1

				if NewRow > RowTracker:
					RowTracker = NewRow

				if NewCol > MaxCol:
					CurrentCol = StartCol
					CurrentRow = RowTracker + RowPadding
				else:
					CurrentCol = NewCol + ColPadding
			#Do plate solution sheet here

	EXCELIO.WriteSheet(Sheet, 2, 2, [["This is the theoretical final volumes in each plate."]])
	EXCELIO.WriteSheet(Sheet, 3, 2, [["Actual volume can be slightly less due to evaporation."]])
	EXCELIO.WriteSheet(Sheet, 4, 2, [["Plates that are not listed have a final volume less than or equal to 0."]])
	
	EXCELIO.Merge(Sheet,2,2,2,TrackedMaxCol)
	EXCELIO.Merge(Sheet,3,2,3,TrackedMaxCol)
	EXCELIO.Merge(Sheet,4,2,4,TrackedMaxCol)
	
	EXCELIO.Center(Sheet,2,2,2,TrackedMaxCol)
	EXCELIO.Center(Sheet,3,2,3,TrackedMaxCol)
	EXCELIO.Center(Sheet,4,2,4,TrackedMaxCol)
	
	EXCELIO.FontSize(Sheet,2,2,2,TrackedMaxCol,18)
	EXCELIO.FontSize(Sheet,3,2,3,TrackedMaxCol,18)
	EXCELIO.FontSize(Sheet,4,2,4,TrackedMaxCol,18)

	for Column in range(1,50):
		EXCELIO.AutoFit(Sheet,Column)	
