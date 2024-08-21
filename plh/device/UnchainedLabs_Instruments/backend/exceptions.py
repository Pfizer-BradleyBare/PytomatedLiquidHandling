from __future__ import annotations


class PlateTypeIncompatibleWithInstrumentError(Exception): ...


class PlateTypeIncompatibleWithApplicationError(Exception): ...


class UnknownPlateTypeInExperimentDefinitionError(Exception): ...


class ApplicationNotInstalledOnInstrumentError(Exception): ...


class FileArgumentNotFoundOrReadableError(Exception): ...


class NotAllArgumentsListedError(Exception): ...


class UnknownCommandError(Exception): ...


class InternalDLLErrorIntegerConversionError(Exception): ...


class InternalDLLErrorStringConversionError(Exception): ...


class CouldNotConnectOverTCPError(Exception): ...


class AutomationLicenseNotActiveError(Exception): ...


class InstrumentInIncorrectStateError(Exception): ...


class NoPlateInInstrumentError(Exception): ...


class ResultsCanOnlyBeExportedIfAllPlatesAreMeasuredError(Exception): ...


class IncorrectArgumentPlateIDAlreadyMeasuredError(Exception): ...


class IncorrectArgumentPlateIDIsNotValidError(Exception): ...


class AccessInterruptedByLocalUserBackendResourceError(Exception): ...


class TimeoutError(Exception): ...


class StoreBlanksMoreThanOneStoredBlankSampleGroupAvailableError(Exception): ...


class StoreBlanksStoredBlankSampleGroupNameIncorrectByNameError(Exception): ...


class StoreBlanksStoredBlankSampleGroupNameIncorrectByColumnError(Exception): ...


class StoreBlanksFileNotFoundError(Exception): ...


class StoreBlanksNoReproducableBlanksFoundError(Exception): ...


class StoreBlanksInstrumentCalibratedSinceBlankExperimentError(Exception): ...


class StoreBlanksExperimentTooLongAgoError(Exception): ...


class StoreBlanksBlankExperimentIsFromADifferentInstrumentError(Exception): ...


class AccessAndConnectionTrayIsMovingError(Exception): ...


class CouldNotPerformCommandMeasurementBusyError(Exception): ...


class AccessAndConnectionMeasurementFailedError(Exception): ...


class AccessAndConnectionMeasurementFailedToInitializeError(Exception): ...


class BarecodeReaderTimeoutError(Exception): ...


class NoBarcodeReaderAvailableError(Exception): ...


class BarcodeNotValidError(Exception): ...


class TimeoutForGoingToOpenTrayPositionError(Exception): ...


class NoSamplesDefinedError(Exception): ...


class NoPumpProfilesError(Exception): ...


class ErrorReadingSamplesError(Exception): ...


class ErrorReadingExperimentDefinitionError(Exception): ...


class TrayNotInRightPositionError(Exception): ...


class CouldNotCloseTrayError(Exception): ...


class CouldNotOpenTrayError(Exception): ...


class NoAccessError(Exception): ...


status_code_map: dict[int, type[Exception]] = {
    -904: PlateTypeIncompatibleWithInstrumentError,
    -903: PlateTypeIncompatibleWithInstrumentError,
    -902: UnknownPlateTypeInExperimentDefinitionError,
    -901: ApplicationNotInstalledOnInstrumentError,
    -401: FileArgumentNotFoundOrReadableError,
    -400: NotAllArgumentsListedError,
    -300: UnknownCommandError,
    -202: InternalDLLErrorIntegerConversionError,
    -201: InternalDLLErrorStringConversionError,
    -200: CouldNotConnectOverTCPError,
    -120: AutomationLicenseNotActiveError,
    -111: InstrumentInIncorrectStateError,
    -106: NoPlateInInstrumentError,
    -104: ResultsCanOnlyBeExportedIfAllPlatesAreMeasuredError,
    -103: IncorrectArgumentPlateIDAlreadyMeasuredError,
    -102: IncorrectArgumentPlateIDIsNotValidError,
    -100: AccessInterruptedByLocalUserBackendResourceError,
    -99: TimeoutError,
    -68: StoreBlanksMoreThanOneStoredBlankSampleGroupAvailableError,
    -67: StoreBlanksStoredBlankSampleGroupNameIncorrectByNameError,
    -66: StoreBlanksStoredBlankSampleGroupNameIncorrectByColumnError,
    -65: StoreBlanksFileNotFoundError,
    -64: StoreBlanksNoReproducableBlanksFoundError,
    -63: StoreBlanksInstrumentCalibratedSinceBlankExperimentError,
    -62: StoreBlanksExperimentTooLongAgoError,
    -61: StoreBlanksBlankExperimentIsFromADifferentInstrumentError,
    -52: AccessAndConnectionTrayIsMovingError,
    -31: CouldNotPerformCommandMeasurementBusyError,
    -24: AccessAndConnectionMeasurementFailedError,
    -22: AccessAndConnectionMeasurementFailedToInitializeError,
    -17: BarecodeReaderTimeoutError,
    -16: NoBarcodeReaderAvailableError,
    -15: BarcodeNotValidError,
    -14: TimeoutForGoingToOpenTrayPositionError,
    -13: NoSamplesDefinedError,
    -12: NoPumpProfilesError,
    -11: NoPumpProfilesError,
    -10: ErrorReadingSamplesError,
    -9: ErrorReadingExperimentDefinitionError,
    -5: TrayNotInRightPositionError,
    -4: CouldNotCloseTrayError,
    -3: CouldNotOpenTrayError,
    -2: InstrumentInIncorrectStateError,
    -1: NoAccessError,
}
