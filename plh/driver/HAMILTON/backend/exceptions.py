# ignore exceptions being invalid module name
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hamilton_response_base import HamiltonBlockData


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
class PressureLLDErrorConsequtiveAspirationError(HamiltonError):
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
    """Overshot of limits during aspirate or dispense.

    Note:
    ----
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
    """Undershot of limits during aspirate or dispense.

    Note:
    ----
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
    """Liquid surface not detected.

    This error is created from main / slave error 06/70, 06/73 and 06/87.
    """


@dataclass(frozen=True)
class NotDetectedError(HamiltonError):
    """Carrier not detected at deck end position."""


@dataclass(frozen=True)
class NotAspiratedError(HamiltonError):
    """Dispense volume exceeds the aspirated volume.

    This error is created from main / slave error 02/54.
    """


@dataclass(frozen=True)
class ImproperDispenseError(HamiltonError):
    """The dispensed volume is out of tolerance (may only occur for Nano Pipettor Dispense steps).

    This error is created from main / slave error 02/52 and 02/54.
    """


@dataclass(frozen=True)
class NoLabwareError(HamiltonError):
    """The labware to be loaded was not detected by autoload module.

    Note:
    ----
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


###CUSTOM BELOW###
@dataclass(frozen=True)
class PeripheralDeviceCommunicationError(HamiltonError):
    """Communication with integrated device failed. This is typically a usb communication error."""


@dataclass(frozen=True)
class GripperPickupError(HamiltonError):
    """This error is common with the Vantage Quad-CORE-Grippers. Currently a software issue in VOV software."""

@dataclass(frozen=True)
class InvalidLabwareID(HamiltonError):
    """The labware ID is not available in the deck layout."""


error_code_map: dict[int, type[HamiltonError]] = {
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
    14: PressureLLDErrorConsequtiveAspirationError,
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
    ###CUSTOM BELOW###
    10001: PeripheralDeviceCommunicationError,
    10002: GripperPickupError,
    10003: InvalidLabwareID
}

error_code_description_map: dict[str, int] = {
    "__TODO__": 2,
    "__TODO__": 3,
    "__TODO__": 4,
    "__TODO__": 5,
    "__TODO__": 6,
    "__TODO__": 7,
    "__TODO__": 8,
    "__TODO__": 9,
    "__TODO__": 10,
    "__TODO__": 11,
    "__TODO__": 12,
    "__TODO__": 13,
    "__TODO__": 14,
    "__TODO__": 15,
    "__TODO__": 16,
    "__TODO__": 17,
    "__TODO__": 18,
    "__TODO__": 19,
    "__TODO__": 20,
    "__TODO__": 21,
    "__TODO__": 22,
    "__TODO__": 23,
    "__TODO__": 24,
    "__TODO__": 25,
    "__TODO__": 26,
    "__TODO__": 27,
    "__TODO__": 28,
    "__TODO__": 29,
    "__TODO__": 30,
    "__TODO__": 31,
    "__TODO__": 32,
    "__TODO__": 33,
    "__TODO__": 99,
    "__TODO__": 100,
    "__TODO__": 101,
    "__TODO__": 102,
    "__TODO__": 103,
    "__TODO__": 104,
    "__TODO__": 105,
    "__TODO__": 106,
    "__TODO__": 107,
    "__TODO__": 108,
    "__TODO__": 109,
    "__TODO__": 110,
    "__TODO__": 111,
    "__TODO__": 112,
    "__TODO__": 113,
    ###CUSTOM BELOW###
    "Peripheral device communication failed": 10001,
    "Gripper did not detect expected labware": 10002,
    "(tip presence check).)\n(0x28 - 0x1 - 0x80a)\n": 10002,
    "LabwareId is invalid for the current deck layout": 10003,
}
