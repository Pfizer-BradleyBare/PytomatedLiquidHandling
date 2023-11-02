from typing import TypeVar
from ..UnchainedLabsCommand import UnchainedLabsCommandABC
from ..UnchainedLabsResponse import UnchainedLabsResponseABC

UnchainedLabsCommandABCType = TypeVar(
    "UnchainedLabsCommandABCType", bound=UnchainedLabsCommandABC
)
UnchainedLabsResponseABCType = TypeVar(
    "UnchainedLabsResponseABCType", bound=UnchainedLabsResponseABC
)

"""
class PlateTypeIncompatibleWithInstrument(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -904"


class PlateTypeIncompatibleWithApplication(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -903"


class UnknownPlateType(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -902"


class ApplicationNotRecognized(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -901"


class FileNotFound(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -401"


class MissingArguments(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -400"


class UnknownCommand(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -300"


class InternalIntegerError(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -202"


class InternalStringError(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -201"


class CouldNotConnectOverTCP(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -200"


class AutomationLicenseNotActive(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -120"


class InstrumentInWrongState1(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -111"


class NoPlateLoaded(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -106"


class AllPlatesNotMeasured(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -104"


class PlateAlreadyMeasured(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -103"


class PlateIDInvalid(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -102"


class LocalConnectionInterrupt(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -100"


class TimeoutGeneral(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -99"


class StoreBlanksAmbiguousGroup(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -68"


class StoreBlanksIncorrectGroupByName(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -67"


class StoreBlanksIncorrectGroupByColumn(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -66"


class StoreBlanksFileNotFound(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -65"


class StoreBlanksNoReproducableBlanks(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -64"


class StoreBlanksInvalidBlanksInstrumentRecalibrated(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -63"


class StoreBlanksTooOld(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -62"


class StoreBlanksWrongInstrument(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -61"


class InstrumentBusyTrayMoving(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -52"


class InstrumentBusyMeasurementOngoing(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -31"


class MeasurementFailedGeneral(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -24"


class MeasurementFailedInitialization(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -22"


class BarecodeReaderTimeout(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -17"


class BarecodeReaderNotInstalled(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -16"


class BarecodeReaderBarcodeNotValid(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -15"


class TimeoutTryOpen(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -14"


class NoSamplesDefined(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -13"


class NoPumpProfiles1(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -12"


class NoPumpProfiles2(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -11"


class ReadErrorSamples(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -10"


class ReadErrorExperiment(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -9"


class IncorrectTrayPosition(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -5"


class CanNotCloseTray(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -4"


class CanNotOpenTray(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -3"


class InstrumentInWrongState2(
    ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]
):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -2"


class NoAccess(ExceptionABC[UnchainedLabsCommandABCType, UnchainedLabsResponseABCType]):
    @classmethod
    def DetailsErrorValue(cls) -> str | int:
        return "Unchained Labs: -1"
"""
