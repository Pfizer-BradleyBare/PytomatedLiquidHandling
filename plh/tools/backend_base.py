from __future__ import annotations

import json
from abc import abstractmethod
from dataclasses import field
from typing import TypeVar, cast

from pydantic import BaseModel, dataclasses

from .command_base import CommandBase
from .response_base import ResponseBase

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseBase)


@dataclasses.dataclass(kw_only=True)
class BackendBase:
    """A base class for all backends."""

    identifier: str
    """A name given to the backend."""

    is_running: bool = field(init=False, default=False)
    """Is the backend running?"""

    @abstractmethod
    def start(self: BackendBase) -> None:
        """Should start the system software then establish communication. You should only call the method once."""
        if self.is_running is True:
            msg = f"{type(self).__name__} backend is already running"
            raise RuntimeError(msg)
        self.is_running = True

    @abstractmethod
    def stop(self: BackendBase) -> None:
        """Should close the communication layer then kill the system software."""
        if self.is_running is False:
            msg = f"{type(self).__name__} backend is not running"
            raise RuntimeError(msg)
        self.is_running = False

    @abstractmethod
    def execute(self: BackendBase, command: CommandBase) -> None:
        """Delivers the ```Command``` to the system to be executed."""
        if self.is_running is False:
            msg = f"{type(self).__name__} backend is not running"
            raise RuntimeError(msg)

    @abstractmethod
    def wait(self: BackendBase, command: CommandBase) -> None:
        """Waits for execution of ```Command``` to complete."""
        if self.is_running is False:
            msg = f"{type(self).__name__} backend is not running"
            raise RuntimeError(msg)

    @abstractmethod
    def acknowledge(
        self: BackendBase,
        command: CommandBase,
        response_type: type[ResponseABCType],
    ) -> ResponseABCType:
        """Returns a response described by ```ResponseType``` for the executed ```Command```.
        Response data is parsed by pydantic into the type specified. You may discard the response.
        NOTE: Exceptions may be raised upon execution. See the specific backend for exception details.
        """
        if self.is_running is False:
            msg = f"{type(self).__name__} backend is not running"
            raise RuntimeError(msg)

    def simple_representation(self) -> str:
        model_load_json = json.loads(BaseModel.model_dump_json(cast(BaseModel, self)))

        def get_id(model_json: dict) -> None:
            for key in model_json:
                value = model_json[key]

                if isinstance(value, list):
                    for index, item in enumerate(value):
                        if isinstance(item, dict) and "identifier" in item:
                            value[index] = item["identifier"]

                if isinstance(value, dict):
                    if "identifier" in value:
                        model_json[key] = value["identifier"]
                    else:
                        get_id(value)

        get_id(model_load_json)

        return json.dumps(model_load_json, indent=4)
