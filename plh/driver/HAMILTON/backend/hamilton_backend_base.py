from __future__ import annotations

import pathlib
import shutil
import subprocess
import time
from dataclasses import field
from platform import platform
from typing import Callable, TypeVar, cast

from flask import request
from loguru import logger
from pydantic import Field, FilePath, dataclasses

from plh.driver.tools import (
    BackendBase,
    BackendServerBase,
    CommandBackendErrorHandlingMixin,
    CommandOptionsListMixin,
)

from .hamilton_command_action_base import HamiltonCommandActionBase
from .hamilton_command_base import HamiltonCommandBase
from .hamilton_command_state_base import HamiltonCommandStateBase
from .hamilton_response_base import HamiltonResponseBase

HamiltonResponseBaseType = TypeVar(
    "HamiltonResponseBaseType",
    bound=HamiltonResponseBase,
)


class Config:
    arbitrary_types_allowed = True


@dataclasses.dataclass(kw_only=True, config=Config)
class HamiltonBackendServer(BackendServerBase):
    views: list[Callable] = field(init=False)

    def __post_init__(self: HamiltonBackendServer) -> None:
        self.views = [self.Execute, self.Acknowledge]
        BackendServerBase.__post_init__(self)

    def Execute(self: HamiltonBackendServer) -> tuple:  # noqa:N802
        bound_logger = logger.bind(Request=request.get_data(), Server=self)
        bound_logger.debug(
            "{server} | Execute web API request.",
            server=self.identifier,
        )

        if request.is_json is False:
            bound_logger.error("Request from Hamilton is not json format.")
            return "Request is not json format.", 400

        content = request.get_json()

        try:
            timeout = content["Timeout"]
        except KeyError:
            bound_logger.exception("Timeout is missing from request.")
            return "Timeout is missing from request.", 400

        timeout -= 10
        counter = 0

        while self._command is None or self._response is not None:
            time.sleep(0.1)
            if counter >= timeout * 10:
                break

        command = cast(HamiltonCommandBase, self._command)

        if command is None:
            return "Command not available. Try again.", 408

        if isinstance(command, CommandOptionsListMixin) and len(command.options) == 0:
            self._response = ValueError(
                "There are no options in the options tracker",
            )
            return self.Execute()
        # This makes sure there are actually options. It could be possible for a user to submit a command with an options tracker without actul options

        response = {}
        bound_logger = bound_logger.bind(Response=response)

        response["Module Name"] = command.module_name
        response["Command Name"] = command.command_name

        if isinstance(command, CommandBackendErrorHandlingMixin):
            response["CustomErrorHandling"] = int(not command.backend_error_handling)

            # Backend error handling true corresponds to Backend Error Handling false.
            # Unfortunately when I wrote the Hamilton backend I used CustomErrorHandling. Too much work to change right now.
            # TODO: change Hamilton libraries to Backend Error Handling

        try:
            with bound_logger.catch(reraise=True):
                response["Command Parameters"] = command.serialize_options()
            # catch the error if it occurs and log it. Then reraise so we can cleanup.
        except KeyError:
            self._response = RuntimeError(
                "Error while converting Options to json dict.",
            )
            return self.Execute()
        # This is a fragile function. Catch errors if they occur...

        bound_logger.debug(
            "Command delivered to Hamilton: {command_name}",
            command_name=command.command_name,
        )

        return response, 200

    def Acknowledge(self: HamiltonBackendServer) -> tuple:  # noqa:N802
        bound_logger = logger.bind(Request=request.get_data(), Server=self)
        bound_logger.debug(
            "{server} | Acknowledge web API request.",
            server=self.identifier,
        )

        if request.is_json is False:
            bound_logger.error("Request from Hamilton is not json format.")
            return "Request is not json format.", 400

        if self._command is None:
            bound_logger.error("There is no active command needing a response.")
            return "There is no active command needing a response.", 400

        if self._response is not None:
            bound_logger.error("Command already has a response.")
            return "Command already has a response.", 400
        # Check the command does not already have a response

        self._response = request.get_json()
        # Add response then release threads waiting for a response

        bound_logger.debug("Response received from Hamilton.")

        return "Response received.", 200


@dataclasses.dataclass(kw_only=True)
class HamiltonBackendBase(BackendBase):
    method: FilePath
    deck_layout: FilePath
    simulation_on: bool
    _action_server: HamiltonBackendServer = field(init=False)
    _state_server: HamiltonBackendServer = field(init=False)
    _hamilton_process: None = field(
        init=False,
        default=Field(exclude=True, default=None),
    )

    def __post_init__(self: HamiltonBackendBase) -> None:
        self._action_server = HamiltonBackendServer(
            identifier=str(self.identifier) + " Action Server",
            sub_domain="/ActionServer/",
            port=767,
        )
        self._state_server = HamiltonBackendServer(
            identifier=str(self.identifier) + " State Server",
            sub_domain="/StateServer/",
            port=768,
        )

    def start(self: HamiltonBackendBase) -> None:
        if "windows" not in platform().lower():
            msg = "Hamilton backend is only supported on Windows PCs. Sorry!"
            raise RuntimeError(msg)

        BackendBase.start(self)

        layout_base_path = pathlib.Path(
            "C:\\Program Files (x86)\\HAMILTON\\Library\\plh\\plh\\driver\\HAMILTON\\backend\\layout\\__active_layout__.lay",
        )
        pathlib.Path(layout_base_path).parent.mkdir(
            mode=777,
            exist_ok=True,
            parents=True,
        )

        if not self.deck_layout.exists():
            raise RuntimeError(
                "Layout File not found. Ensure the layout file exists in this location: "
                + str(self.deck_layout),
            )
        shutil.copyfile(self.deck_layout, layout_base_path)
        shutil.copyfile(
            self.deck_layout.with_suffix(".res"),
            layout_base_path.with_suffix(".res"),
        )
        # Move layout file into temp folder. Layouts are comprised of 2 files: .lay, and .res

        hamilton_config = "C:\\Program Files (x86)\\HAMILTON\\Config\\HxServices.cfg"

        process = subprocess.Popen(
            [  # noqa:S603
                "C:\\Program Files (x86)\\HAMILTON\\Bin\\HxCfgFilConverter.exe",
                "/t",
                hamilton_config,
            ],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        # Taken from PyVenus by SNIPR Biome. Thank you!!

        while process.poll() is None:
            ...
        # Wait for completion

        with pathlib.Path(hamilton_config).open() as file:
            contents = (
                file.read()
                .replace(
                    'SimulationOn, "1",',
                    'SimulationOn, "' + str(int(self.simulation_on)) + '",',
                )
                .replace(
                    'SimulationOn, "0",',
                    'SimulationOn, "' + str(int(self.simulation_on)) + '",',
                )
            )
        with pathlib.Path(hamilton_config).open(mode="w") as file:
            file.write(contents)
        # Turn on or off simulation mode

        self._HamiltonProcess = subprocess.Popen(
            [  # noqa: S603
                "C:\\Program Files (x86)\\HAMILTON\\Bin\\HxRun.exe",
                "-t",
                self.method,
            ],
        )

        self._action_server.start()
        self._state_server.start()

    def stop(self: HamiltonBackendBase) -> None:
        BackendBase.stop(self)

        class AbortCommand(HamiltonCommandActionBase):
            ...

        command = AbortCommand()
        self._action_server._command = command  # noqa:SLF001
        self._action_server.wait(command)

        self._action_server.stop()
        self._state_server.stop()

    def execute(
        self: HamiltonBackendBase,
        command: HamiltonCommandActionBase | HamiltonCommandStateBase,
    ) -> None:
        BackendBase.execute(self, command)
        if isinstance(command, HamiltonCommandStateBase):
            self._state_server.execute(command)
        else:
            self._action_server.execute(command)

    def wait(
        self: HamiltonBackendBase,
        command: HamiltonCommandActionBase | HamiltonCommandStateBase,
    ) -> None:
        BackendBase.wait(self, command)

        if isinstance(command, HamiltonCommandStateBase):
            server = self._state_server
        else:
            server = self._action_server

        while server._response is None:  # noqa: SLF001
            if self._HamiltonProcess.poll() is not None:
                ...
        # If the process closed then we need to reopen it (MAYBE). Only the script can close the Hamilton.
        # TODO: This should be done differently but not sure how yet.

    def acknowledge(
        self: HamiltonBackendBase,
        command: HamiltonCommandActionBase | HamiltonCommandStateBase,
        response_type: type[HamiltonResponseBaseType],
    ) -> HamiltonResponseBaseType:
        BackendBase.acknowledge(self, command, response_type)
        if isinstance(command, HamiltonCommandStateBase):
            response = self._state_server.acknowledge(command, response_type)

        else:
            response = self._action_server.acknowledge(command, response_type)

        return response
