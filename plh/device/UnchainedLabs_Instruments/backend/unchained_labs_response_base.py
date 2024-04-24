from __future__ import annotations

import dataclasses
from enum import Enum

from plh.device.tools import ResponseBase

from .exceptions import status_code_map


class StatusCodes(Enum):
    successful = 0
    access_already_acheived = 1
    tray_already_open = 3
    tray_already_closed = 4
    access_and_connection_free = 20
    access_and_connection_no_measurement = 21
    access_and_connection_measurement_started = 23
    access_and_connection_measurement_successful = 25
    access_and_connection_measurement_initializing = 30
    access_and_connection_measurement_busy = 31
    access_and_connection_load_next_plate = 32
    access_and_connection_measurement_paused = 33
    access_and_connection_tray_is_open = 50
    access_and_connection_tray_is_closed = 51
    access_and_connection_tray_is_moving = 52
    client_exit_accepted = 999


@dataclasses.dataclass(kw_only=True)
class UnchainedLabsResponseBase(ResponseBase):
    status_code_raw: dataclasses.InitVar[tuple | int]
    status_code: StatusCodes = dataclasses.field(init=False)

    def __post_init__(
        self: UnchainedLabsResponseBase,
        status_code_raw: tuple | int,
    ) -> None:
        if isinstance(status_code_raw, tuple):
            status_code_raw_int = status_code_raw[0]
        else:
            status_code_raw_int = status_code_raw

        self.StatusCode = StatusCodes(status_code_raw_int)

        if status_code_raw_int < 0:
            raise status_code_map[status_code_raw_int]
