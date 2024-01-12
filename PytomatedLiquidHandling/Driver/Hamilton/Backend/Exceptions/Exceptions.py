from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from ..HamiltonResponse import HamiltonBlockData


@dataclass(frozen=True)
class HamiltonError(Exception):
    HamiltonBlockData: HamiltonBlockData | None


@dataclass(frozen=True)
class HardwareError(HamiltonError):
    """Steps lost on one or more hardware components, or component not initialized or not functioning."""


@dataclass(frozen=True)
class NotExecutedError(HamiltonError):
    """There was an error in previous part command."""


@dataclass(frozen=True)
class ClotError(HamiltonError):
    """Blood clot detected."""


@dataclass(frozen=True)
class BarcodeError(HamiltonError):
    """Barcode could not be read or is missing."""


@dataclass(frozen=True)
class InsufficientLiquidError(HamiltonError):
    """Not enough liquid available."""


@dataclass(frozen=True)
class TipPresentError(HamiltonError):
    """A tip has already been picked up."""


@dataclass(frozen=True)
class NoTipError(HamiltonError):
    """Tip is missing or not picked up."""


@dataclass(frozen=True)
class NoCarrierError(HamiltonError):
    """No carrier present for loading."""


@dataclass(frozen=True)
class ExecutionError(HamiltonError):
    """A step or a part of a step could not be processed."""


@dataclass(frozen=True)
class PressureLLDError(HamiltonError):
    """A dispense with pressure liquid level detection is not allowed."""


@dataclass(frozen=True)
class CalibrateError(HamiltonError):
    """No capacitive signal detected during carrier calibration procedure."""


@dataclass(frozen=True)
class UnloadError(HamiltonError):
    """Not possible to unload the carrier due to occupied loading tray position."""


@dataclass(frozen=True)
class PressureLLDErrorConsequtiveAspiration(HamiltonError):
    """Pressure liquid level detection in a consecutive aspiration is not allowed."""


@dataclass(frozen=True)
class ParameterError(HamiltonError):
    """Dispense in jet mode with pressure liquid level detection is not allowed."""


@dataclass(frozen=True)
class CoverOpenError(HamiltonError):
    """Cover not closed or can not be locked."""


@dataclass(frozen=True)
class ImproperAspirationDispenseError(HamiltonError):
    """The pressure-based aspiration / dispensation control reported an error ( not enough liquid )."""


@dataclass(frozen=True)
class WashLiquidError(HamiltonError):
    """Waste full or no more wash liquid available."""


@dataclass(frozen=True)
class TemperatureError(HamiltonError):
    """Incubator temperature out of range."""


@dataclass(frozen=True)
class TADMOvershotError(HamiltonError):
    """
    Overshot of limits during aspirate or dispense.

    Note:

    DO NOT USE THIS ERROR. Instead use the following:

    On aspirate this error is returned as main error 17 (ImproperAspirationDispenseError).

    On dispense this error is returned as main error 4 (ClotError).
    """


@dataclass(frozen=True)
class LabwareError(HamiltonError):
    """Labware not available."""


@dataclass(frozen=True)
class LabwareGrippedError(HamiltonError):
    """Labware already gripped."""


@dataclass(frozen=True)
class LabwareLostError(HamiltonError):
    """Labware lost during transport."""


@dataclass(frozen=True)
class IllegalTargetPlatePositionError(HamiltonError):
    """Cannot place plate, plate was gripped in a wrong direction."""


@dataclass(frozen=True)
class IllegalInterventionError(HamiltonError):
    """Cover was opened or a carrier was removed manually."""


@dataclass(frozen=True)
class TADMUndershotError(HamiltonError):
    """
    Undershot of limits during aspirate or dispense.

    Note:

    DO NOT USE THIS ERROR. Instead use the following:

    On aspirate this error is returned as main error 4 (ClotError).

    On dispense this error is returned as main error 17 (ImproperAspirationDispenseError).
    """


@dataclass(frozen=True)
class PositionError(HamiltonError):
    """The position is out of range."""


@dataclass(frozen=True)
class UnexpectedcLLDError(HamiltonError):
    """The cLLD detected a liquid level above start height of liquid level search."""


@dataclass(frozen=True)
class AreaAlreadyOccupiedError(HamiltonError):
    """Instrument region already reserved."""


@dataclass(frozen=True)
class ImpossibleToOccupyAreaError(HamiltonError):
    """A region on the instrument cannot be reserved."""


@dataclass(frozen=True)
class AntiDropControlError(HamiltonError):
    """Anti drop controlling out of tolerance."""


@dataclass(frozen=True)
class DecapperError(HamiltonError):
    """Decapper lock error while screw / unscrew a cap by twister channels."""


@dataclass(frozen=True)
class DecapperHandlingError(HamiltonError):
    """Decapper station error while lock / unlock a cap."""


@dataclass(frozen=True)
class SlaveError(HamiltonError):
    """Slave error. Unknown."""


@dataclass(frozen=True)
class WrongCarrierError(HamiltonError):
    """Wrong carrier barcode detected."""


@dataclass(frozen=True)
class NoCarrierBarcodeError(HamiltonError):
    """Carrier barcode could not be read or is missing."""


@dataclass(frozen=True)
class LiquidLevelError(HamiltonError):
    """
    Liquid surface not detected.

    This error is created from main / slave error 06/70, 06/73 and 06/87.
    """


@dataclass(frozen=True)
class NotDetectedError(HamiltonError):
    """Carrier not detected at deck end position."""


@dataclass(frozen=True)
class NotAspiratedError(HamiltonError):
    """
    Dispense volume exceeds the aspirated volume.

    This error is created from main / slave error 02/54.
    """


@dataclass(frozen=True)
class ImproperDispenseError(HamiltonError):
    """
    The dispensed volume is out of tolerance (may only occur for Nano Pipettor Dispense steps).

    This error is created from main / slave error 02/52 and 02/54.
    """


@dataclass(frozen=True)
class NoLabwareError(HamiltonError):
    """
    The labware to be loaded was not detected by autoload module.

    Note:

    May only occur on a Reload Carrier step if the labware property 'MlStarCarPosAreRecognizable' is set to 1.
    """


@dataclass(frozen=True)
class UnexpectedLabwareError(HamiltonError):
    """The labware contains unexpected barcode ( may only occur on a Reload Carrier step )."""


@dataclass(frozen=True)
class WrongLabwareError(HamiltonError):
    """The labware to be reloaded contains wrong barcode ( may only occur on a Reload Carrier step )."""


@dataclass(frozen=True)
class BarcodeMaskError(HamiltonError):
    """The barcode read doesn't match the barcode mask defined."""


@dataclass(frozen=True)
class BarcodeNotUniqueError(HamiltonError):
    """The barcode read is not unique. Previously loaded labware with same barcode was loaded without unique barcode check."""


@dataclass(frozen=True)
class BarcodeAlreadyUsedError(HamiltonError):
    """The barcode read is already loaded as unique barcode ( it's not possible to load the same barcode twice )."""


@dataclass(frozen=True)
class KitLotExpiredError(HamiltonError):
    """Kit Lot expired."""


@dataclass(frozen=True)
class DelimiterError(HamiltonError):
    """Barcode contains character which is used as delimiter in result string."""


ExceptionErrorCodeMap: dict[int, Type[HamiltonError]] = {
    2: HardwareError,
    3: NotExecutedError,
    4: ClotError,
    5: BarcodeError,
    6: InsufficientLiquidError,
    7: TipPresentError,
    8: NoTipError,
    9: NoCarrierError,
    10: ExecutionError,
    11: PressureLLDError,
    12: CalibrateError,
    13: UnloadError,
    14: PressureLLDErrorConsequtiveAspiration,
    15: ParameterError,
    16: CoverOpenError,
    17: ImproperAspirationDispenseError,
    18: WashLiquidError,
    19: TemperatureError,
    20: TADMOvershotError,
    21: LabwareError,
    22: LabwareGrippedError,
    23: LabwareLostError,
    24: IllegalTargetPlatePositionError,
    25: IllegalInterventionError,
    26: TADMUndershotError,
    27: PositionError,
    28: UnexpectedcLLDError,
    29: AreaAlreadyOccupiedError,
    30: ImpossibleToOccupyAreaError,
    31: AntiDropControlError,
    32: DecapperError,
    33: DecapperHandlingError,
    99: SlaveError,
    100: WrongCarrierError,
    101: NoCarrierBarcodeError,
    102: LiquidLevelError,
    103: NotDetectedError,
    104: NotAspiratedError,
    105: ImproperDispenseError,
    106: NoLabwareError,
    107: UnexpectedLabwareError,
    108: WrongLabwareError,
    109: BarcodeMaskError,
    110: BarcodeNotUniqueError,
    111: BarcodeAlreadyUsedError,
    112: KitLotExpiredError,
    113: DelimiterError,
}

ErrorCodeDescriptionMap: dict[str, int] = {
    "": 2,
    "": 3,
    "": 4,
    "": 5,
    "": 6,
    "": 7,
    "": 8,
    "": 9,
    "": 10,
    "": 11,
    "": 12,
    "": 13,
    "": 14,
    "": 15,
    "": 16,
    "": 17,
    "": 18,
    "": 19,
    "": 20,
    "": 21,
    "": 22,
    "": 23,
    "": 24,
    "": 25,
    "": 26,
    "": 27,
    "": 28,
    "": 29,
    "": 30,
    "": 31,
    "": 32,
    "": 33,
    "": 99,
    "": 100,
    "": 101,
    "": 102,
    "": 103,
    "": 104,
    "": 105,
    "": 106,
    "": 107,
    "": 108,
    "": 109,
    "": 110,
    "": 111,
    "": 112,
    "": 113,
}
