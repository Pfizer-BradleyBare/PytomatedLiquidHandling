from enum import Enum
import copy
from ..Steps import Steps as STEPS
from ...General import ExcelIO as EXCELIO
from ...User import Samples as SAMPLES

class LabwareTypes(Enum):
    Plate = "Plate"
    Reagent = "Reagent"

ViscosityVolatilityValues = {"Low":{"Weight":1,"Value":1},"Medium":{"Weight":1,"Value":2},"High":{"Weight":1,"Value":3},"Very High":{"Weight":1,"Value":4}}
HomogeneityValues = {"Homogenous":{"Weight":1,"Value":1},"Heterogenous":{"Weight":1,"Value":2},"Suspension":{"Weight":1,"Value":3},"Emulsion":{"Weight":1,"Value":4}}
#This wil


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
        self.LiquidClassString = None


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
    def GetLiquidClassString(self):
        raise NotImplementedError() #this is a crude implementation of virtual functions

    def UpdateLabwareSolutionParameters(self):
        LabwareName = self.GetLabwareName()
        self.Category = ExcelSolutionInfoDict[LabwareName]["Category"]
        self.StorageTemperature = ExcelSolutionInfoDict[LabwareName]["StorageTemperature"]
        self.Viscosity = ExcelSolutionInfoDict[LabwareName]["Viscosity"]
        self.Volatility = ExcelSolutionInfoDict[LabwareName]["Volatility"]
        self.Homogeneity = ExcelSolutionInfoDict[LabwareName]["Homogeneity"]
        self.LiquidClassString = ExcelSolutionInfoDict[LabwareName]["LiquidClassString"]

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

    for Row in range(0,10,8):
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
            LiquidClassString = Output[Row + 6][Column + 1]
            
            if LiquidClassString == "Custom (Advanced Only)":
                LiquidClassString = "None"
            #if the liquid class is the custom value then the user probably doesn't know what they are doing. Change it to None
            
            SolutionNames = SAMPLES.Column(SolutionName)
            for SolutionName in SolutionNames:
                ExcelSolutionInfoDict[SolutionName] = {"Category":Category,"StorageTemperature": StorageTemperature, "Volatility":Volatility, "Viscosity":Viscosity,"Homogeneity":Homogeneity,"LiquidClassString":LiquidClassString}
        if BreakFlag == True:
            break