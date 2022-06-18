from ..Steps import Plate as PLATE
from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
from ...User import Configuration as CONFIGURATION
from ..Labware import Labware as LABWARE
from ..Labware import Solutions as SOLUTIONS
import copy
import time

class PipetteSequence:
	def __init__ (self):
		self.Destinations = []
		self.DestinationPositions = []
		self.Sources = []
		self.SourcePositions = []
		self.TransferVolumes = []
		self.CurrentDestinationVolumes = []
		self.AspirateCycles = []
		self.DispenseCycles = []
		self.SourceLiquidClassStrings = []
		self.DestinationLiquidClassStrings = []
		self.SourceLLDValues = []
		self.DestinationLLDValues = []

	def GetDestinations(self):
		return self.Destinations

	def GetDestinationPositions(self):
		return self.DestinationPositions

	def GetSources(self):
		return self.Sources

	def GetSourcePositions(self):
		return self.SourcePositions

	def GetTransferVolumes(self):
		return self.TransferVolumes

	def GetCurrentDestinationVolumes(self):
		return self.CurrentDestinationVolumes

	def GetAspirateCycles(self):
		return self.AspirateCycles

	def GetDispenseCycles(self):
		return self.DispenseCycles

	def GetSourceLiquidClassStrings(self):
		return self.SourceLiquidClassStrings

	def GetDestinationLiquidClassStrings(self):
		return self.DestinationLiquidClassStrings

	def GetSourceLLDValues(self):
		return self.SourceLLDValues

	def GetDestinationLLDValues(self):
		return self.DestinationLLDValues

	def GetNumSequencePositions(self):
		return len(self.GetDestinationPositions())

	def AppendToPipetteSequence(self,Dest,DestPos,Source,SourcePos,Vol,CurDestVol,AspirateCycles,DispenseCycles,SourceLiquidClassString, DestinationLiquidClassString,SourceLLDValue, DestinationLLDValue):
		Index = 0
		for Counter in range(0,self.GetNumSequencePositions()):

			if Dest == self.GetDestinations()[Counter] and DestPos == self.GetDestinationPositions()[Counter] and SourcePos == self.GetSourcePositions()[Counter] and Source == self.GetSources()[Counter]:
				self.GetTransferVolumes()[Counter] += Vol
				return

			if DestPos > self.GetDestinationPositions()[Counter]:
				Index = Counter + 1

		self.Destinations.insert(Index,Dest)
		self.DestinationPositions.insert(Index,DestPos)
		self.Sources.insert(Index,Source)
		self.SourcePositions.insert(Index,SourcePos)
		self.TransferVolumes.insert(Index,Vol)
		self.CurrentDestinationVolumes.insert(Index,CurDestVol)
		self.AspirateCycles.insert(Index,AspirateCycles)
		self.DispenseCycles.insert(Index,DispenseCycles)
		self.SourceLiquidClassStrings.insert(Index,SourceLiquidClassString)
		self.DestinationLiquidClassStrings.insert(Index,DestinationLiquidClassString)
		self.SourceLLDValues.insert(Index,SourceLLDValue)
		self.DestinationLLDValues.insert(Index,DestinationLLDValue)

class Class(LABWARE.Class):
######################################################################### 
#	Description: Initializes class to default starting parameters
#	Input Arguments: [PlateName: String] [Type: String] [SequencesList: List]
#	Returns: N/A
#########################################################################
	def __init__ (self, Name, PlateType):
		LABWARE.Class.__init__(self, Name, LABWARE.LabwareTypes.Plate)
		self.IsPreloaded = False
		self.PlateType = PlateType
		self.PipetteVolumesList = []
		self.VolumesList = [0] * SAMPLES.GetNumSamples()
		self.MaxVolumeList = [0] * SAMPLES.GetNumSamples()
		self.MinVolumeList = [0] * SAMPLES.GetNumSamples()
		self.WellContents = [[] for _ in range(SAMPLES.GetNumSamples())]

	#
	# Preloaded functions
	#
	def SetIsPreloaded(self):
		self.IsPreloaded = True
	def GetIsPreloaded(self):
		return self.IsPreloaded

	#
	# This is the type of plate. 96 Well or some other form. This is dependant on the user config.
	#
	def GetPlateType(self):
		return self.PlateType

    #
    #  All recorded pipetting volumes for this particular labware
    #
	def AddPipetteVolume(self, Volume):
		self.PipetteVolumesList.append(Volume)
	def GetPipetteVolumesList(self):
		return self.PipetteVolumesList


	#
	# Implemented Virtual function from Labware class
	#
	def GetMaxVolume(self):
		return max(self.MaxVolumeList)

	#
	# This should be called everytime there is a change to the plate. This allows us to capture the historical min and max volumes of the plate
	#
	def DoVolumeUpdate(self):
		CurrentVolumeList = self.VolumesList
		MinVolumeList = self.MinVolumeList
		MaxVolumeList = self.MaxVolumeList

		for VolumeIndex in range(0,len(CurrentVolumeList)):
			
			if CurrentVolumeList[VolumeIndex] < MinVolumeList[VolumeIndex]:
				MinVolumeList[VolumeIndex] = CurrentVolumeList[VolumeIndex]
			#min volume is the most negative value ever acquired in the plate

			Volume = abs(CurrentVolumeList[VolumeIndex])
			if Volume > MaxVolumeList[VolumeIndex]:
				MaxVolumeList[VolumeIndex] = Volume
			#Max volume is the absolute max value

	#
	# This adjusts the well contents by a decimal percentage for each well
	#
	def UpdateWellContents(self, Well, DecimalPercentage):
		RemoveList = []
		for Content in Well:
			Content["Volume"] *= DecimalPercentage
			if Content["Volume"] == 0:
				RemoveList.append(Content)
		for Item in RemoveList:
			Well.remove(Item)

	#
	# This is a generic implementation to cover Viscosity, Volatility, and Homogeneity
	#
	def GenericCalculation(self, SampleIndex, DefaultValue, ValuesDict, PlatesGetFunction, SolutionsGetFunction):

		WellContents = self.WellContents[SampleIndex]
		TotalVolume = self.VolumesList[SampleIndex]

		if len(WellContents) == 0 or TotalVolume == 0:
			return DefaultValue


		Calculation = []
		for Content in WellContents:
			SolutionLabware = LABWARE.GetLabware(Content["Solution"])
			SolutionWellPosition = Content["Well"]
			SolutionPercentage = int(Content["Volume"] / TotalVolume * 100)
			
			if SolutionLabware.GetLabwareType() == LABWARE.LabwareTypes.Plate:
				Value = PlatesGetFunction(SolutionLabware, SolutionWellPosition)
			else:
				Value = SolutionsGetFunction(SolutionLabware, SolutionWellPosition)
			ValuesDictItem = ValuesDict[Value]

			Calculation += [ValuesDictItem["Value"]] * SolutionPercentage * ValuesDictItem["Weight"]
				#why do we add the number SolutionPercentage times? Because the high the percentage the higher contribution to the new value.
		#So what are we doing here? We are calculating the contribution each solution gives to the overall composition of the well.

		WellComposition = int(round(sum(Calculation) / len(Calculation)))

		for Key in ValuesDict:
			if WellComposition == ValuesDict[Key]["Value"]:
				return Key



	def GetCategory(self):
		return "Plate"
	def GetStorageTemperature(self):
		return "Ambient"
	def GetViscosity(self, SampleIndex):
		self.UpdateLabwareSolutionParameters()
		return self.GenericCalculation(SampleIndex,self.Viscosity,LABWARE.ViscosityValues, Class.GetViscosity, SOLUTIONS.Class.GetViscosity)
	def GetVolatility(self, SampleIndex):
		self.UpdateLabwareSolutionParameters()
		return self.GenericCalculation(SampleIndex,self.Volatility,LABWARE.VolatilityValues, Class.GetVolatility, SOLUTIONS.Class.GetVolatility)
	def GetHomogeneity(self, SampleIndex):
		self.UpdateLabwareSolutionParameters()
		return self.GenericCalculation(SampleIndex,self.Homogeneity,LABWARE.HomogeneityValues, Class.GetHomogeneity, SOLUTIONS.Class.GetHomogeneity)
	def GetLLD(self, SampleIndex):
		self.UpdateLabwareSolutionParameters()
		return self.GenericCalculation(SampleIndex,self.LLD,LABWARE.LLDValues, Class.GetLLD, SOLUTIONS.Class.GetLLD)
				
######################################################################### 
#	Description: Creates a sorted pipetting list to be used by the hamilton pipette command
#	Input Arguments: [SourceList: List] [SourceVolumeList: List]
#	Returns: [List of Lists]
#########################################################################
def CreatePipetteSequence(DestinationContextStringsList, DestinationNamesList, SourceContextStringsList, SourceNamesList, SourceVolumesList, AspirateList, DispenseList, RecordPipetteVolumes=True):
	
	StartPosition = SAMPLES.GetStartPosition()

	NewSequence = PipetteSequence()

	for SampleIndex in range(0,len(DestinationNamesList)):

		DestinationContextString = DestinationContextStringsList[SampleIndex]
		DestinationName = DestinationNamesList[SampleIndex]
		SourceContextString = SourceContextStringsList[SampleIndex]
		SourceName = SourceNamesList[SampleIndex]
		Volume = SourceVolumesList[SampleIndex]
		Aspirate = AspirateList[SampleIndex]
		Dispense = DispenseList[SampleIndex]
		
		DestinationLabware = LABWARE.GetLabware(DestinationName)

		DestinationSequencePosition = LABWARE.GetContextualSequences(DestinationContextString)[SampleIndex]

		ContextFlags = LABWARE.GetContextualFlags(DestinationContextString)
		if "SequenceFromPlateStart" in ContextFlags:
			DestinationArrayPosition = DestinationSequencePosition - 1
			DestinationLabware.SetIsPlateStartSequence()
		else:
			DestinationArrayPosition = DestinationSequencePosition - StartPosition
		#This is a case where the Pool can modify the sequence position to be at the start of the plate instead of the user chosen posiiton.
		#We need the array position because that tells us which volume to modify and which factors to use.
		#The array position is derived from the Sequence Position

		CurrentWellVolume = DestinationLabware.VolumesList[DestinationArrayPosition]
		PipettingFactor = LABWARE.GetContextualFactors(DestinationContextStringsList[SampleIndex])[DestinationArrayPosition]

		ActualVolume = Volume * PipettingFactor

		if ActualVolume > 0:
			
			SourceSequencePosition = DestinationSequencePosition
			SourceArrayPosition = SourceSequencePosition

			SourceLabware = LABWARE.GetLabware(SourceName)
			if SourceLabware == None:
				SourceLabware = SOLUTIONS.Class(SourceName)
				LABWARE.AddLabware(SourceLabware)
			#If the labware doesn't exists then it has to be a reagent. Add it

			if SourceLabware.GetLabwareType() == LABWARE.LabwareTypes.Reagent:
				SOLUTIONS.Class.AddVolume(SourceLabware, ActualVolume)

				SourceViscosityCriteria = SourceLabware.GetViscosity(SampleIndex)
				SourceVolatilityCriteria = SourceLabware.GetVolatility(SampleIndex)
				SourceHomogeneityCriteria = SourceLabware.GetHomogeneity(SampleIndex)
				SourceLLDCriteria = SourceLabware.GetLLD(SampleIndex)
				#We need to get the solution properties first then we can determine mixing based off that

			elif SourceLabware.GetLabwareType() == LABWARE.LabwareTypes.Plate:
				SourceSequencePosition = LABWARE.GetContextualSequences(SourceContextString)[SampleIndex]
				ContextFlags = LABWARE.GetContextualFlags(SourceContextString)
				if "SequenceFromPlateStart" in ContextFlags:
					SourceArrayPosition = SourceSequencePosition - 1
					SourceLabware.SetIsPlateStartSequence()
				else:
					SourceArrayPosition = SourceSequencePosition - StartPosition
				#This is a case where the aliquot can modify the sequence position to be at the start of the plate instead of the user chosen posiiton.

				SourceViscosityCriteria = SourceLabware.GetViscosity(SourceArrayPosition)
				SourceVolatilityCriteria = SourceLabware.GetVolatility(SourceArrayPosition)
				SourceHomogeneityCriteria = SourceLabware.GetHomogeneity(SourceArrayPosition)
				SourceLLDCriteria = SourceLabware.GetLLD(SourceArrayPosition)
				#We need to get the solution properties first then we can determine mixing based off that

				Volume = SourceLabware.VolumesList[SourceArrayPosition]
				NewVolume = Volume - ActualVolume
				PercentChange = NewVolume / Volume
				Well = SourceLabware.WellContents[SourceArrayPosition]
				SourceLabware.UpdateWellContents(Well, PercentChange)
				#Update the contents in the well

				SourceLabware.VolumesList[SourceArrayPosition] = NewVolume
				SourceLabware.DoVolumeUpdate()
			#Do plate volume subtraction

			DestinationLabware.WellContents[DestinationArrayPosition].append({"Solution":SourceName, "Well":SourceArrayPosition, "Volume":ActualVolume})
			DestinationLabware.VolumesList[DestinationArrayPosition] += ActualVolume
			DestinationLabware.DoVolumeUpdate()
			#Add the solution to the wells

			DestinationViscosityCriteria = DestinationLabware.GetViscosity(DestinationArrayPosition)
			DestinationVolatilityCriteria = DestinationLabware.GetVolatility(DestinationArrayPosition)
			DestinationHomogeneityCriteria = DestinationLabware.GetHomogeneity(DestinationArrayPosition)
			DestinationLLDCriteria = DestinationLabware.GetLLD(DestinationArrayPosition)
			#We want to calculate the Destination properties "after" the source has been added, that way we can determine the proper mixing params.

			AspirateCycles = LABWARE.DetermineMaxMixingParam(Aspirate,SourceViscosityCriteria,SourceVolatilityCriteria,SourceHomogeneityCriteria,SourceLLDCriteria,"Aspirate")
			AspirateLiquidClass = "Viscosity" + SourceViscosityCriteria + "Volatility" + SourceVolatilityCriteria + "Homogeneity" + SourceHomogeneityCriteria
			#Calculate source mixing first (This is aspiration) and the source liquid class string

			DispenseCycles = LABWARE.DetermineMaxMixingParam(Dispense,DestinationViscosityCriteria,DestinationVolatilityCriteria,DestinationHomogeneityCriteria,DestinationLLDCriteria,"Dispense")
			DispenseLiquidClass = "Viscosity" + DestinationViscosityCriteria + "Volatility" + DestinationVolatilityCriteria + "Homogeneity" + DestinationHomogeneityCriteria
			#Then calculate destination (This is Dispense)

			NewSequence.AppendToPipetteSequence(DestinationName,DestinationSequencePosition,SourceName,SourceSequencePosition,ActualVolume,CurrentWellVolume,AspirateCycles,DispenseCycles,AspirateLiquidClass,DispenseLiquidClass,SourceLLDCriteria,DestinationLLDCriteria)
	
	if RecordPipetteVolumes == True:
		for Volume in NewSequence.GetTransferVolumes():
			Class.AddPipetteVolume(DestinationLabware,Volume)

	return copy.deepcopy(NewSequence)

def GetAllPipetteVolumes():
	PipetteVolumesList = []
	for Plate in LABWARE.GetAllLabwareType(LABWARE.LabwareTypes.Plate):
		PipetteVolumesList += Plate.GetPipetteVolumesList()
	return PipetteVolumesList