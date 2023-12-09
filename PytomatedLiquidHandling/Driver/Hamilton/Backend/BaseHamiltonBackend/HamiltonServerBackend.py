from loguru import logger
import time
from dataclasses import field
from typing import Callable, cast
from flask import request
from pydantic import dataclasses

from ....Tools.BaseClasses import CommandOptionsListed, ServerBackendABC
from ..HamiltonCommand import HamiltonCommandABC


@dataclasses.dataclass(kw_only=True)
class HamiltonServerBackendABC(ServerBackendABC):
    Views: list[Callable] = field(init=False)

    def __post_init__(self) -> None:
        self.Views = [self.GetNextCommand, self.RespondToCommand]
        ServerBackendABC.__post_init__(self)

    def GetNextCommand(self):
        BoundLogger = logger.bind(Request=request.get_data())

        if request.is_json == False:
            BoundLogger.error("Request from Hamilton is not json format.")
            return dict(Response="Request is not json format.")

        Content = request.get_json()

        try:
            Timeout = Content["Timeout"]
        except KeyError:
            BoundLogger.error("Timeout is missing from request.")
            return dict(Response="Timeout is missing from request.")

        Timeout -= 10
        Counter = 0

        while self._Command is None or self._Response is not None:
            if Counter >= Timeout * 10:
                break

            time.sleep(0.1)

        Command = cast(HamiltonCommandABC, self._Command)

        if Command is None:
            return dict(Response="Command not available. Try again.")

        if isinstance(Command, CommandOptionsListed):
            if len(Command.Options) == 0:
                self._Response = ValueError(
                    "There are no options in the options tracker"
                )
                return self.GetNextCommand()
        # This makes sure there are actually options. It could be possible for a user to submit a command with an options tracker without actul options

        Response = dict()

        if hasattr(Command, "BackendErrorHandling"):
            Response["CustomErrorHandling"] = (
                not not not getattr(Command, "BackendErrorHandling"),
            )
            # Backend error handling true corresponds to Backend Error Handling false.
            # Unfortunately when I wrote the Hamilton backend I used CustomErrorHandling. Too much work to change right now.
            # TODO: change Hamilton libraries to Backend Error Handling

        Response["Module Name"] = Command.ModuleName
        Response["Command Name"] = Command.CommandName

        try:
            with BoundLogger.catch(reraise=True, level="critical"):
                Response["Command Parameters"] = Command.SerializeOptions()
            # catch the error if it occurs and log it. Then reraise so we can cleanup.
        except:
            self._Response = RuntimeError(
                "Error while converting Options to json dict."
            )
            return self.GetNextCommand()
        # This is a fragile function. Catch errors if they occur...

        return dict(Response=Response)

    def RespondToCommand(self):
        BoundLogger = logger.bind(Request=request.get_data())

        if request.is_json == False:
            BoundLogger.error("Request from Hamilton is not json format.")
            return dict(Response="Request is not json format.")

        if self._Command is None:
            BoundLogger.error("There is no active command needing a response.")
            return dict(Response="There is no active command needing a response.")

        if self._Response is not None:
            BoundLogger.error("Command already has a response.")
            return dict(Response="Command already has a response.")
        # Check the command does not already have a response

        self._Response = request.get_json()
        # Add response then release threads waiting for a response

        return dict(Response="Response received.")
