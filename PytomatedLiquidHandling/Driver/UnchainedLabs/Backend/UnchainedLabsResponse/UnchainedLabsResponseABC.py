from enum import Enum
from typing import Any

import dataclasses

from ....Tools.BaseClasses import ResponseABC
from ..Exceptions import ExceptionStatusCodeMap


@dataclasses.dataclass(kw_only=True)
class UnchainedLabsResponseABC(ResponseABC):
    class StatusCodes(Enum):
        Successful = 0
        AccessAlreadyAcheived = 1
        TrayAlreadyOpen = 3
        TrayAlreadyClosed = 4
        AccessAndConnectionFree = 20
        AccessAndConnectionNoMeasurement = 21
        AccessAndConnectionMeasurementStarted = 23
        AccessAndConnectionMeasurementSuccessful = 25
        AccessAndConnectionMeasurementInitializing = 30
        AccessAndConnectionMeasurementBusy = 31
        AccessAndConnectionLoadNextPlate = 32
        AccessAndConnectionMeasurementPaused = 33
        AccessAndConnectionTrayIsOpen = 50
        AccessAndConnectionTrayIsClosed = 51
        AccessAndConnectionTrayIsMoving = 52
        ClientExitAccepted = 999

    StatusCodeRaw: dataclasses.InitVar[tuple | int]
    StatusCodeParsed: StatusCodes = dataclasses.field(init=False)

    def __post_init__(self, StatusCodeRaw):
        if isinstance(StatusCodeRaw, tuple):
            StatusCodeRaw = StatusCodeRaw[0]

        self.StatusCodeParsed = StatusCodeRaw

        if StatusCodeRaw < 0:
            raise ExceptionStatusCodeMap[StatusCodeRaw]
