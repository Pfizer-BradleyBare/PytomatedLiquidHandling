from enum import Enum

class LabwareTypes(Enum):
    Plate = "Plate"
    Reagent = "Reagent"


LabwareList = []

class Class:   
    def __init__(self, NameString, LabwareType):
        self.LabwareName = NameString
        self.LabwareType = LabwareType
        self.IsLoaded = False
        self.IsVacuum = False
        self.IsIMCSSizeXDesalting = False
        self.MaxVolume = 0

    #
    # This is labware info
    #
    def GetLabwareName(self):
        return self.LabwareName
    def GetLabwareType(self):
        return self.LabwareType

    #
    # This is a flag that indicates wether or not this labware is to be loaded automatically
    #
    def SetIsLoaded(self):
        self.IsLoaded = True
    def GetIsLoaded(self):
        return self.IsLoaded

    #
    # This is a flag which indicates whether or not this plate is used on a vacuum
    #
    def SetIsVacuum(self):
        self.IsVacuum = True
    def GetIsVacuum(self):
        return self.IsVacuum

    #
    # This is a flag which indicates whether or not this plate is used for desalting
    #
    def SetIsIMCSSizeXDesalting(self):
        self.IsIMCSSizeXDesalting = True
    def GetIsIMCSSizeXDesalting(self):
        return self.IsIMCSSizeXDesalting
    
    #
    # This tracks the max volume used in this labware
    #
    def SetMaxVolume(self, MaxVolume):
        self.MaxVolume = MaxVolume
    def GetMaxVolume(self):
        return self.MaxVolume
    
