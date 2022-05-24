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
	StartRow = 2
	StartCol = 2
	MaxCol = 11
	CurrentRow = StartRow
	CurrentCol = StartCol
	RowPadding = 2
	ColPadding = 2
	RowTracker = 0

	#Sequences = CONFIGURATION.GetAutoloadingSequences()

	try:
		EXCELIO.DeleteSheet("PrepList")
	except:
		pass

	EXCELIO.CreateSheet("PrepList")

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
								PlatePrepArray[int(position)] = {"AlphaNumeric":position,"Volume":abs(PlateLoadedVolumeList[index])}
							else:
								PlatePrepArray[int(position)] = {"AlphaNumeric":position,"Volume":abs(PlateLoadedVolumeList[index]) + LabwareArray[LabwareName]["Labware Info"]["Dead Volume"]}
				
				if len(PlatePrepArray) != 0:
					UsedSpace = EXCELIO.PrintPlate(CurrentRow, CurrentCol, LabwareName, LabwareArray[LabwareName]["Labware Name"], LabwareArray[LabwareName]["Labware Info"]["Labware Rows"], LabwareArray[LabwareName]["Labware Info"]["Labware Columns"], PlatePrepArray)

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
			if True:

				UsedSpace = EXCELIO.PrintReagent(CurrentRow, CurrentCol, LabwareName, LabwareArray[LabwareName]["Labware Name"], LabwareArray[LabwareName]["Used Volume"])

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

	for Column in range(1,15):
		EXCELIO.AutoFit("PrepList",Column)	





