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
		self.Mix = []
		self.LiquidClassString = []

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

	def GetMixCriteria(self):
		return self.Mix

	def GetLiquidClassStrings(self):
		return self.LiquidClassString

	def GetNumSequencePositions(self):
		return len(self.GetDestinationPositions())

	def AppendToPipetteSequence(self,Dest,DestPos,Source,SourcePos,Vol,CurDestVol,Mix,LiquidClassString):
		Index = 0
		for Counter in range(0,self.GetNumSequencePositions()):
			if DestPos > self.GetDestinationPositions()[Counter]:
				Index = Counter + 1

		self.Destinations.insert(Index,Dest)
		self.DestinationPositions.insert(Index,DestPos)
		self.Sources.insert(Index,Source)
		self.SourcePositions.insert(Index,SourcePos)
		self.TransferVolumes.insert(Index,Vol)
		self.CurrentDestinationVolumes.insert(Index,CurDestVol)
		self.Mix.insert(Index,Mix)
		self.LiquidClassString.insert(Index,LiquidClassString)

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
	# This is a generic implementation to cover Viscosity, Volatility, and Homogeneity
	#
	def GenericCalculation(self, SampleIndex, DefaultValue, ValuesDict, PlatesGetFunction, SolutionsGetFunction):
		WellContents = self.WellContents[SampleIndex]
		
		if len(WellContents) == 0:
			return DefaultValue
		
		TotalVolume = self.VolumesList[SampleIndex]

		Calculation = []
		for Content in WellContents:
			SolutionLabware = LABWARE.GetLabware(Content["Solution"])
			SolutionPercentage = int(Content["Volume"] / TotalVolume * 100)
			
			if SolutionLabware.GetLabwareType() == LABWARE.LabwareTypes.Plate:
				Value = PlatesGetFunction(SolutionLabware, SampleIndex)
			else:
				Value = SolutionsGetFunction(SolutionLabware, SampleIndex)
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
		return self.GenericCalculation(SampleIndex,self.Viscosity,LABWARE.ViscosityVolatilityValues, Class.GetViscosity, SOLUTIONS.Class.GetViscosity)
	def GetVolatility(self, SampleIndex):
		self.UpdateLabwareSolutionParameters()
		return self.GenericCalculation(SampleIndex,self.Volatility,LABWARE.ViscosityVolatilityValues, Class.GetVolatility, SOLUTIONS.Class.GetVolatility)
	def GetHomogeneity(self, SampleIndex):
		self.UpdateLabwareSolutionParameters()
		return self.GenericCalculation(SampleIndex,self.Homogeneity,LABWARE.HomogeneityValues, Class.GetHomogeneity, SOLUTIONS.Class.GetHomogeneity)
	def GetLiquidClassString(self):
		self.UpdateLabwareSolutionParameters()
		return self.LiquidClassString
				
######################################################################### 
#	Description: Creates a sorted pipetting list to be used by the hamilton pipette command
#	Input Arguments: [SourceList: List] [SourceVolumeList: List]
#	Returns: [List of Lists]
#########################################################################
def CreatePipetteSequence(DestinationContextStringsList, DestinationNamesList, SourceContextStringsList, SourceNamesList, SourceVolumesList, MixingList, RecordPipetteVolumes=True):
	
	StartPosition = SAMPLES.GetStartPosition()

	NewSequence = PipetteSequence()

	for SampleIndex in range(0,len(DestinationNamesList)):

		DestinationContextString = DestinationContextStringsList[SampleIndex]
		DestinationName = DestinationNamesList[SampleIndex]
		SourceContextString = SourceContextStringsList[SampleIndex]
		SourceName = SourceNamesList[SampleIndex]
		Volume = SourceVolumesList[SampleIndex]
		MixParameter = MixingList[SampleIndex]
		
		DestinationLabware = LABWARE.GetLabware(DestinationName)

		DestinationSequencePosition = LABWARE.GetContextualSequences(DestinationContextString)[SampleIndex]
		DestinationArrayPosition = DestinationSequencePosition - StartPosition
		#We need the array position because that tells us which volume to modify and which factors to use.
		#The array position is derived from the Sequence Position

		CurrentWellVolume = DestinationLabware.VolumesList[DestinationArrayPosition]
		PipettingFactor = LABWARE.GetContextualFactors(DestinationContextStringsList[SampleIndex])[DestinationArrayPosition]

		ActualVolume = Volume * PipettingFactor

		if ActualVolume > 0:
			
			SourceSequencePosition = DestinationSequencePosition

			SourceLabware = LABWARE.GetLabware(SourceName)
			if SourceLabware == None:
				SourceLabware = SOLUTIONS.Class(SourceName)
				LABWARE.AddLabware(SourceLabware)
			#If the labware doesn't exists then it has to be a reagent. Add it
			
			SourceLiquidClassString = SourceLabware.GetLiquidClassString()
			if SourceLiquidClassString == "None":
				LiquidClassString = "Vicosity" + SourceLabware.GetViscosity(SampleIndex)
				LiquidClassString += "Volatility" + SourceLabware.GetVolatility(SampleIndex)
				LiquidClassString += "Homogeneity" + SourceLabware.GetHomogeneity(SampleIndex)
			else:
				LiquidClassString = "__CUSTOM__" + SourceLiquidClassString

			if SourceLabware.GetLabwareType() == LABWARE.LabwareTypes.Reagent:
				SOLUTIONS.Class.AddVolume(SourceLabware, ActualVolume)

			elif SourceLabware.GetLabwareType() == LABWARE.LabwareTypes.Plate:
				SourceSequencePosition = LABWARE.GetContextualSequences(SourceContextString)[SampleIndex]
				SourceArrayPosition = SourceSequencePosition - StartPosition
				SourceLabware.VolumesList[SourceArrayPosition] -= ActualVolume
				SourceLabware.DoVolumeUpdate()
				#DestinationLabware.WellContents[DestinationArrayPosition].append({"Solution":"__REMOVE__","Volume":ActualVolume})
			#Do plate volume subtraction

			if RecordPipetteVolumes == True:
				Class.AddPipetteVolume(DestinationLabware,ActualVolume)
			DestinationLabware.WellContents[SampleIndex].append({"Solution":SourceName,"Volume":ActualVolume})
			
			NewSequence.AppendToPipetteSequence(DestinationName,DestinationSequencePosition,SourceName,SourceSequencePosition,ActualVolume,CurrentWellVolume,MixParameter,LiquidClassString)
				
			DestinationLabware.VolumesList[DestinationArrayPosition] += ActualVolume
			DestinationLabware.DoVolumeUpdate()

	return copy.deepcopy(NewSequence)

def GetAllPipetteVolumes():
	PipetteVolumesList = []
	for Plate in LABWARE.GetAllLabwareType(LABWARE.LabwareTypes.Plate):
		PipetteVolumesList += Plate.GetPipetteVolumesList()
	return PipetteVolumesList