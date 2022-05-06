from ..Steps import Plate as PLATE
from ..Steps import Steps as STEPS
from ...User import Samples as SAMPLES
from ...User import Configuration as CONFIGURATION
from ..Labware import Labware as LABWARE
from ..Labware import Solutions as SOLUTIONS
import copy

class PipetteSequence:
	def __init__ (self):
		self.Destinations = []
		self.DestinationPositions = []
		self.Sources = []
		self.SourcePositions = []
		self.TransferVolumes = []
		self.CurrentDestinationVolumes = []
		self.Mix = []

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

	def GetNumSequencePositions(self):
		return len(self.GetDestinationPositions())

	def AppendToPipetteSequence(self,Dest,DestPos,Source,SourcePos,Vol,CurDestVol,Mix):
		Index = 0
		for Counter in range(0,self.GetNumSequencePositions()):
			if DestPos > self.GetDestinationPositions()[Counter]:
				Index = Counter + 1

		self.GetDestinations().insert(Index,Dest)
		self.GetDestinationPositions().insert(Index,DestPos)
		self.GetSources().insert(Index,Source)
		self.GetSourcePositions().insert(Index,SourcePos)
		self.GetTransferVolumes().insert(Index,Vol)
		self.GetCurrentDestinationVolumes().insert(Index,CurDestVol)
		self.GetMixCriteria().insert(Index,Mix)

class Class(LABWARE.Class):
######################################################################### 
#	Description: Initializes class to default starting parameters
#	Input Arguments: [PlateName: String] [Type: String] [SequencesList: List]
#	Returns: N/A
#########################################################################
	def __init__ (self, Name, PlateType):
		LABWARE.Class.__init__(self, Name, LABWARE.LabwareTypes.Plate)
		self.PlateType = PlateType
		self.VolumesList = [0] * SAMPLES.GetNumSamples()
		self.MaxVolumeList = [0] * SAMPLES.GetNumSamples()
		self.MinVolumeList = [0] * SAMPLES.GetNumSamples()

	#
	# This is the type of plate. 96 Well or some other form. This is dependant on the user config.
	#
	def GetPlateType(self):
		return self.PlateType

	#
	# Implemented Virtual function from Labware class
	#
	def GetMaxVolume(self):
		return max(self.MaxVolumeList)

	#
	# This will return the context for the plate in the current pathway
	#
	def GetPlateContextualString(self,Step):
		SearchStep = Step
		PlateName = LABWARE.Class.GetLabwareName(self)
		while True:
			SearchStep = STEPS.GetPreviousStepInPathway(SearchStep)
			if STEPS.Class.GetParentPlateName(SearchStep) == PlateName:
				return STEPS.Class.GetContext(SearchStep)
		#This should technically never fail
		
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
				
######################################################################### 
#	Description: Creates a sorted pipetting list to be used by the hamilton pipette command
#	Input Arguments: [SourceList: List] [SourceVolumeList: List]
#	Returns: [List of Lists]
#########################################################################
	def CreatePipetteSequence(self, DestinationContextStringsList, SourceContextStringsList, SourcesList, SourceVolumesList, MixingList):
		
		NewSequence = PipetteSequence()

		DestinationVolumesList = self.VolumesList

		for SampleIndex in range(0,len(DestinationVolumesList)):

			Factor = SAMPLES.GetContextualFactors(DestinationContextStringsList[SampleIndex])[SampleIndex]
			DestinationSequencesList = SAMPLES.GetContextualSequences(DestinationContextStringsList[SampleIndex])[SampleIndex]

			DestinationName = LABWARE.Class.GetLabwareName(self)
			SourceName = SourcesList[SampleIndex]
			Volume = SourceVolumesList[SampleIndex]
			CurrentWellVolume = DestinationVolumesList[SampleIndex]
			MixParameter = MixingList[SampleIndex]

			ActualVolume = Volume * Factor

			if ActualVolume > 0:
			
				SourceSequencesList = DestinationSequencesList

				SourceLabware = LABWARE.GetLabware(SourceName)
				if SourceLabware == None:
					SourceLabware = SOLUTIONS.Class(SourceName)
					LABWARE.AddLabware(SourceLabware)
				#If the labware doesn't exists then it has to be a reagent. Add it
				
				if SourceLabware.GetLabwareType() == LABWARE.LabwareTypes.Reagent:
					SOLUTIONS.Class.AddVolume(SourceLabware)

				elif SourceLabware.GetLabwareType() == LABWARE.LabwareTypes.Plate:
					SourceLabware.VolumesList[SampleIndex] -= ActualVolume
					SourceLabware.DoVolumeUpdate()
					SourceSequencesList = SAMPLES.GetContextualSequences(SourceContextStringsList[SampleIndex])
				#Do plate volume subtraction

				for SequenceIndex in range(0,len(DestinationSequencesList)):
					DestinationSequencePosition = DestinationSequencesList[SequenceIndex]
					SourceSequencePosition = SourceSequencesList[SequenceIndex]

					NewSequence.AppendToPipetteSequence(DestinationName,DestinationSequencePosition,SourceName,SourceSequencePosition,ActualVolume,CurrentWellVolume,MixParameter)
				
				DestinationVolumesList[SampleIndex] += ActualVolume
				self.DoVolumeUpdate()

		return copy.deepcopy(NewSequence)

