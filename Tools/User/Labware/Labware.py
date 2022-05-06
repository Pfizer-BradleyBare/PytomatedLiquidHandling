from enum import Enum
import copy

class LabwareTypes(Enum):
    Plate = "Plate"
    Reagent = "Reagent"

LabwareSet = set()

class Class:   
    def __init__(self, NameString, LabwareType):
        self.LabwareName = NameString
        self.LabwareType = LabwareType
        self.IsVacuum = False
        self.IsIMCSSizeXDesalting = False
        self.IsCovered = False

        #This is here for book keeping perposes. This will actually be pulled or calculated for the method in real time as requested. 
        # Each time it is pulled/calculated these values will be updated
        self.Category = None
        self.StorageCondition = None
        self.Volatility = None
        self.Viscosity = None
        self.Homogeneity = None
        #Book keeping
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
    def SetIsVacuum(self):
        self.IsVacuum = True
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
        self.Lid = True
    def GetIsCovered(self):
        return self.Lid

    #
    # This tracks the max volume used in this labware
    #
    def GetMaxVolume(self):
        raise NotImplementedError() #this is a crude implementation of virtual functions

    #
    # This exposes the Labware Parameters. This must be implemented by the inheriting class
    #
    def GetLabwareParameters(self):
        raise NotImplementedError() #this is a crude implementation of virtual functions

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
    return Labware