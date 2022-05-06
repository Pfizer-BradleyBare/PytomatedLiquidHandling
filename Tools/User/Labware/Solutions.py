
from ..Steps import Steps as STEPS
from ..Steps import Liquid_Transfer as LIQUID_TRANSFER
from ..Steps import Dilute as DILUTE
from ..Steps import Desalt as DESALT
from ...User import Samples as SAMPLES
from ..Labware import Labware as LABWARE
from ...User import Configuration as CONFIGURATION

class Class(LABWARE.Class):
	def __init__(self, Name):
		LABWARE.Class.__init__(self, Name, LABWARE.LabwareTypes.Reagent)
		self.TotalVolume = 0
		self.PipetteVolumesList = []

	#
	# This updates the total volume but also adds the volume as a unique pipetting volume. This will allow the automation system to calculate required tips
	#
	def AddVolume(self, Volume):
			self.TotalVolume += Volume
			self.PipetteVolumesList.append(Volume)

	def GetMaxVolume(self):
		return self.TotalVolume
	
	def GetPipetteVolumesList(self):
		return self.GetPipetteVolumesList






