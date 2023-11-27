from enum import Enum
from typing import Any

from pydantic import field_validator

from ....Tools.AbstractClasses import ResponseABC
from ..Exceptions import ExceptionStatusCodeMap


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

    StatusCode: StatusCodes

    @field_validator("StatusCode", mode="before")
    def __StatusCodeValidate(cls, v):
        if v < 0:
            raise ExceptionStatusCodeMap[v]

        return v
