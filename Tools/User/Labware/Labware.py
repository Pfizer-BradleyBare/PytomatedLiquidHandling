from enum import Enum
import copy
from ..Steps import Steps as STEPS
from ...General import ExcelIO as EXCELIO
from ...User import Samples as SAMPLES

class LabwareTypes(Enum):
    Plate = "Plate"
    Reagent = "Reagent"

##################################
##################################
# Dynamic Mixing and Calc Values #
##################################
##################################
#The following dicts guide dynamic plate value calculations and provide minimum and maximum mixing criteria for each value
#NOTE: The list is in order from least to greatest
ViscosityValues = {\
    "Low":{"Weight":1, "Value":1, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "Medium":{"Weight":1, "Value":2, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "High":{"Weight":1, "Value":3, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "Very High":{"Weight":1, "Value":4, "Minimum Mixing":{"Aspirate":0, "Dispense":0}}\
    }

VolatilityValues = {\
    "Low":{"Weight":1, "Value":1, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "Medium":{"Weight":1, "Value":2, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "High":{"Weight":1, "Value":3, "Minimum Mixing":{"Aspirate":3, "Dispense":0}},\
    "Very High":{"Weight":1, "Value":4, "Minimum Mixing":{"Aspirate":3, "Dispense":0}}\
    }

HomogeneityValues = {\
    "Homogenous":{"Weight":1, "Value":1, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "Heterogenous":{"Weight":1, "Value":2, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "Suspension":{"Weight":1, "Value":3, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "Emulsion":{"Weight":1, "Value":4, "Minimum Mixing":{"Aspirate":0, "Dispense":0}}\
    }

LLDValues = {\
    "Normal":{"Weight":1, "Value":1, "Minimum Mixing":{"Aspirate":0, "Dispense":0}},\
    "Organic":{"Weight":1, "Value":2, "Minimum Mixing":{"Aspirate":5, "Dispense":0}},\
    }
##################################
##################################
# Dynamic Mixing and Calc Values #
##################################
##################################

def DetermineMaxMixingParam(UserMixingCycles, ViscosityCriteria, VolatilityCriteria, HomogeneityCriteria, LLDCriteria, Key):
    MixingArray = []
    MixingArray.append(UserMixingCycles)
    MixingArray.append(ViscosityValues[ViscosityCriteria]["Minimum Mixing"][Key])
    MixingArray.append(VolatilityValues[VolatilityCriteria]["Minimum Mixing"][Key])
    MixingArray.append(HomogeneityValues[HomogeneityCriteria]["Minimum Mixing"][Key])
    MixingArray.append(LLDValues[LLDCriteria]["Minimum Mixing"][Key])
    return max(MixingArray)

class Class:   
    def __init__(self, NameString, LabwareType):
        self.LabwareName = NameString
        self.LabwareType = LabwareType
        self.IsVacuum = False
        self.IsIMCSSizeXDesalting = False
        self.IsCovered = False

        self.PlateStartSequence = False

        self.Category = None
        self.StorageTemperature = None
        self.Viscosity = None
        self.Volatility = None
        self.Homogeneity = None
        self.LLD = None


    #
    # This is labware info
    #
    def GetLabwareName(self):
        return self.LabwareName
    def GetLabwareType(self):
        return self.LabwareType

    #
    # This is a flag which indicates whether or not this labware is used on a vacuum
    #
    def SetIsVacuum(self, VacuumPlateString):
        self.IsVacuum = VacuumPlateString
    def GetIsVacuum(self):
        return self.IsVacuum

    #
    # This is a flag which indicates whether or not this labware is used for desalting
    #
    def SetIsIMCSSizeXDesalting(self):
        self.IsIMCSSizeXDesalting = True
    def GetIsIMCSSizeXDesalting(self):
        return self.IsIMCSSizeXDesalting
    
	#
	# This is a flag which indicates whether or not this labware needs a lid
	#
    def SetIsCovered(self):
        self.IsCovered = True
    def GetIsCovered(self):
        return self.IsCovered

    #
    # This is a flag which indicates that spceial aspiration calcs should be performed
    #
    def SetIsPlateStartSequence(self):
        self.PlateStartSequence = True
    def GetIsPlateStartSequence(self):
        return self.PlateStartSequence

    #
    # This tracks the max volume used in this labware
    #
    def GetMaxVolume(self):
        raise NotImplementedError() #this is a crude implementation of virtual functions

    #
    # Virtual getter functions for solution args
    #
    def GetCategory(self):
        raise NotImplementedError() #this is a crude implementation of virtual functions
    def GetStorageTemperature(self):
        raise NotImplementedError() #this is a crude implementation of virtual functions
    def GetViscosity(self, SampleIndex):
        raise NotImplementedError() #this is a crude implementation of virtual functions
    def GetVolatility(self, SampleIndex):
        raise NotImplementedError() #this is a crude implementation of virtual functions
    def GetHomogeneity(self, SampleIndex):
        raise NotImplementedError() #this is a crude implementation of virtual functions
    def GetLLD(self, SampleIndex):
        raise NotImplementedError() #this is a crude implementation of virtual functions

    def UpdateLabwareSolutionParameters(self):
        LabwareName = self.GetLabwareName()
        try:
            self.Category = ExcelSolutionInfoDict[LabwareName]["Category"]
            self.StorageTemperature = ExcelSolutionInfoDict[LabwareName]["StorageTemperature"]
            self.Viscosity = ExcelSolutionInfoDict[LabwareName]["Viscosity"]
            self.Volatility = ExcelSolutionInfoDict[LabwareName]["Volatility"]
            self.Homogeneity = ExcelSolutionInfoDict[LabwareName]["Homogeneity"]
            self.LLD = ExcelSolutionInfoDict[LabwareName]["LLD"]
        except:
            pass
        #We calculate for both Source and destination. The destination may not have an entry in this dict. So we need to account for that

ContextualFactors_Dict = {}
def SetContextualFactors(ContextString, FactorsList):
    ContextualFactors_Dict[ContextString] = FactorsList
def GetContextualFactors(ContextString):
    return ContextualFactors_Dict[ContextString]
def GetDefaultFactors():
    return [1] * SAMPLES.GetNumSamples()

ContextualSequences_Dict = {}
def SetContextualSequences(ContextString, SequencesList):
	ContextualSequences_Dict[ContextString] = SequencesList
def GetContextualSequences(ContextString):
	return ContextualSequences_Dict[ContextString]
def GetDefaultSequences(StartPosition):
    return list(range(StartPosition,StartPosition + SAMPLES.GetNumSamples()))

ContextualFlags_Dict = {}
def AddContextualFlag(ContextString, FlagString):
    try:
        ContextualFlags_Dict[ContextString] += "," + FlagString
    except:
        ContextualFlags_Dict[ContextString] = FlagString
def RemoveContextualFlag(ContextString, FlagString):
    ContextualFlags_Dict[ContextString] = ContextualFlags_Dict[ContextString].replace(FlagString,"")
def GetContextualFlags(ContextString):
    return ContextualFlags_Dict[ContextString]

#
# Init
#
LabwareSet = set()
def Init():
    global LabwareSet
    SetContextualFactors("",GetDefaultFactors())
    SetContextualSequences("",GetDefaultSequences(SAMPLES.GetStartPosition()))
    AddContextualFlag("","")
    LabwareSet = set()

#
# This will add a labware item to the tracked labware list
#
def AddLabware(Labware):
    if GetLabware(Class.GetLabwareName(Labware)) == None:
        LabwareSet.add(Labware)
    else:
        raise KeyError(f'Value already exists')
#
# This retrieves a labware item
#
def GetLabware(LabwareName):
    for Labware in LabwareSet:
        if Labware.GetLabwareName() == LabwareName:
            return Labware
    return None

#
# This returns all labware as a list
#
def GetAllLabware():
    return LabwareSet

#
#This retrievs labware of a given LabwareTypes Enum item
#
def GetAllLabwareType(LabwareType):
    OutputList = []
    for Labware in LabwareSet:
        if Labware.GetLabwareType() == LabwareType:
            if LabwareType == LabwareTypes.Reagent:
                if Labware.GetMaxVolume() != 0:
                    OutputList.append(Labware)
            else:
                OutputList.append(Labware)
    return OutputList

#
# This will give a list of contexts for a given list of labware. It works for both Reagents and Plates. 
# Be aware, Reagents do not have context so None will be returned 
#
def GetContextualStringsList(Step, LabwareNamesList):
    ContextsList = [False] * len(LabwareNamesList)

    for LabwareIndex in range(0, len(LabwareNamesList)):
        Labware = GetLabware(LabwareNamesList[LabwareIndex])
        if Labware == None or Class.GetLabwareType(Labware) == LabwareTypes.Reagent:
            ContextsList[LabwareIndex] = None
    
    SearchStep = Step
    while True:
        for LabwareIndex in range(0,len(LabwareNamesList)):
            if ContextsList[LabwareIndex] == False and STEPS.Class.GetParentPlateName(SearchStep) == LabwareNamesList[LabwareIndex]:
                ContextsList[LabwareIndex] = STEPS.Class.GetContext(SearchStep)
            #This should technically never fail because we are only searching for plates. Plates must exists somewhere as a parent plate
        
        if not False in ContextsList:
            return ContextsList
        
        SearchStep = STEPS.GetPreviousStepInPathway(SearchStep)

#
# 
#
ExcelSolutionInfoDict = {}
def GetExcelLabwareInfo():
    Output = EXCELIO.Pull("Solutions",2,2,1000,12,2)
    BreakFlag = False

    for Row in range(0,1000,8):
        for Column in range(0,10,4):
            SolutionName = Output[Row][Column]
            if SolutionName == None:
                BreakFlag = True
                break
           
            SolutionName = SolutionName.replace(" - (Click Here to Update)","")
            Category = Output[Row + 1][Column + 1]
            StorageTemperature = Output[Row + 2][Column + 1]
            Volatility = Output[Row + 3][Column + 1]
            Viscosity = Output[Row + 4][Column + 1]
            Homogeneity = Output[Row + 5][Column + 1]
            LLD = Output[Row + 6][Column + 1]
            
            SolutionNames = SAMPLES.Column(SolutionName)
            for SolutionName in SolutionNames:
                ExcelSolutionInfoDict[SolutionName] = {"Category":Category,"StorageTemperature": StorageTemperature, "Volatility":Volatility, "Viscosity":Viscosity,"Homogeneity":Homogeneity,"LLD":LLD}
        if BreakFlag == True:
            break