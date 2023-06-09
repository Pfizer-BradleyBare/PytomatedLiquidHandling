from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, TypeVar

from ....Tools.AbstractClasses import CommandABC

CommandSelf = TypeVar("CommandSelf", bound="UnchainedLabsCommandABC")


@dataclass(kw_only=True)
class UnchainedLabsCommandABC(CommandABC):
    Identifier: str | int = field(default="None")

    @dataclass
    class Response(CommandABC.Response):
        @CommandABC.Response.Decorator_ExpectedResponseProperty
        def GetMeasurementInfo(self) -> str:
            ...

    @classmethod
    def ParseResponse(cls, Response: Any) -> CommandABC.Response:
        if isinstance(Response, int):
            StatusCode = Response
            MeasurementInfo = ""
        elif isinstance(Response, tuple):
            StatusCode = Response[0]
            MeasurementInfo = Response[1]
        else:
            raise Exception("This should never happen")

        if StatusCode < 0:
            State = False
        else:
            State = True

        ResponseInstance = CommandABC.Response()
        ResponseInstance.SetProperty("State", State)
        ResponseInstance.SetProperty("Details", "Unchained Labs: " + str(StatusCode))
        ResponseInstance.SetProperty("MeasurementInfo", MeasurementInfo)

        return ResponseInstance

    @abstractmethod
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        ...

    @dataclass
    class PlateTypeIncompatibleWithInstrument(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -904"

    @dataclass
    class PlateTypeIncompatibleWithApplication(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -903"

    @dataclass
    class UnknownPlateType(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -902"

    @dataclass
    class ApplicationNotRecognized(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -901"

    @dataclass
    class FileNotFound(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -401"

    @dataclass
    class MissingArguments(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -400"

    @dataclass
    class UnknownCommand(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -300"

    @dataclass
    class InternalIntegerError(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -202"

    @dataclass
    class InternalStringError(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -201"

    @dataclass
    class CouldNotConnectOverTCP(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -200"

    @dataclass
    class AutomationLicenseNotActive(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -120"

    @dataclass
    class InstrumentInWrongState1(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -111"

    @dataclass
    class NoPlateLoaded(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -106"

    @dataclass
    class AllPlatesNotMeasured(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -104"

    @dataclass
    class PlateAlreadyMeasured(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -103"

    @dataclass
    class PlateIDInvalid(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -102"

    @dataclass
    class LocalConnectionInterrupt(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -100"

    @dataclass
    class TimeoutGeneral(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -99"

    @dataclass
    class StoreBlanksAmbiguousGroup(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -68"

    @dataclass
    class StoreBlanksIncorrectGroupByName(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -67"

    @dataclass
    class StoreBlanksIncorrectGroupByColumn(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -66"

    @dataclass
    class StoreBlanksFileNotFound(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -65"

    @dataclass
    class StoreBlanksNoReproducableBlanks(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -64"

    @dataclass
    class StoreBlanksInvalidBlanksInstrumentRecalibrated(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -63"

    @dataclass
    class StoreBlanksTooOld(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -62"

    @dataclass
    class StoreBlanksWrongInstrument(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -61"

    @dataclass
    class InstrumentBusyTrayMoving(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -52"

    @dataclass
    class InstrumentBusyMeasurementOngoing(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -31"

    @dataclass
    class MeasurementFailedGeneral(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -24"

    @dataclass
    class MeasurementFailedInitialization(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -22"

    @dataclass
    class BarecodeReaderTimeout(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -17"

    @dataclass
    class BarecodeReaderNotInstalled(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -16"

    @dataclass
    class BarecodeReaderBarcodeNotValid(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -15"

    @dataclass
    class TimeoutTryOpen(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -14"

    @dataclass
    class NoSamplesDefined(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -13"

    @dataclass
    class NoPumpProfiles1(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -12"

    @dataclass
    class NoPumpProfiles2(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -11"

    @dataclass
    class ReadErrorSamples(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -10"

    @dataclass
    class ReadErrorExperiment(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -9"

    @dataclass
    class IncorrectTrayPosition(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -5"

    @dataclass
    class CanNotCloseTray(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -4"

    @dataclass
    class CanNotOpenTray(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -3"

    @dataclass
    class InstrumentInWrongState2(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -2"

    @dataclass
    class NoAccess(CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "Unchained Labs: -1"
