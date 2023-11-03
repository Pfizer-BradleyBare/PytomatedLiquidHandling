from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice


class CarrierABC(HALDevice):
    TrackStart: int
    TrackEnd: int
    NumLabwarePositions: int
    ImagePath3D: str
    ImagePath2D: str
