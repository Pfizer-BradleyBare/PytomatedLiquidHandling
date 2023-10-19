from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject


class CarrierABC(HALObject):
    TrackStart: int
    TrackEnd: int
    NumLabwarePositions: int
    ImagePath3D: str
    ImagePath2D: str
