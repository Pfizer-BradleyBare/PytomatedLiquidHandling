from loguru import logger
import logging
import time
from dataclasses import field
from threading import Event, Thread
from typing import Callable, ClassVar

from flask import Flask
from pydantic import dataclasses

from .SimpleBackendABC import SimpleBackendABC


@dataclasses.dataclass(kw_only=True)
class ServerBackendABC(SimpleBackendABC):
    """Creates a web API for communication with the system software."""

    __Hosts: ClassVar[list[tuple]] = list()
    """Currently running web API hosts"""

    Address: str = "localhost"
    """Web address to request web API endpoints."""

    Port: int = 8080
    """Web port to request web API endpoints."""

    SubDomain: str = "/"
    """Web sub domain to request web API endpoints."""

    Views: list[Callable]
    """Endpoints that the web API exposes."""

    _App: Flask = field(init=False)
    _AppParentThreadRunnerFlag: Event = field(init=False)

    def __post_init__(self) -> None:
        """Creates the web API based on ```Address```, ```Port```, ```SubDomain```, and ```Views```."""
        self._AppParentThreadRunnerFlag = Event()

        self._App = Flask(str(self.Identifier))
        logging.getLogger("werkzeug").disabled = True

        self.Views += [self.IsActive, self.Kill]
        self._App.add_url_rule(self.SubDomain, "Index", self.Index)
        for View in self.Views:
            self._App.add_url_rule(
                self.SubDomain + View.__name__,
                View.__name__,
                View,
                methods=["GET", "POST"],
            )

    def __ServerThreadRunner(self):
        Thread(
            name="Flask App Thread-> " + str(self.Identifier),
            target=self.__Run,
            daemon=True,
        ).start()

        self._AppParentThreadRunnerFlag.wait()
        time.sleep(1)

    def __Run(self):
        self._App.run(self.Address, self.Port)

    def _GetEndpointID(self, Endpoint: str):
        return self.__class__.__name__ + ": " + str(self.Identifier) + "-> " + Endpoint

    def StartBackend(self):
        """- Checks that host is available. If host is not available then raises ```ValueError```.
        - Starts server as daemon thread."""
        SimpleBackendABC.StartBackend(self)
        Host = (self.Address, self.Port)
        if Host in ServerBackendABC.__Hosts:
            raise ValueError(
                "This host is already taken. Choose a different address and/or port."
            )

        ServerBackendABC.__Hosts.append(Host)

        self._AppParentThreadRunnerFlag.clear()

        Thread(
            name="Flask App Thread Runner-> " + str(self.Identifier),
            target=self.__ServerThreadRunner,
        ).start()

    def StopBackend(self):
        """Kills server and all daemon threads. NOTE: expect 1 second delay. If server is not running then raises ```RuntimeError```."""
        SimpleBackendABC.StopBackend(self)
        Host = (self.Address, self.Port)
        if Host not in ServerBackendABC.__Hosts:
            raise RuntimeError("This backend not currently running. Run it first")

        self._AppParentThreadRunnerFlag.set()

        ServerBackendABC.__Hosts.remove(Host)

    def Index(self):
        """Index API endpoint."""
        BoundLogger = logger.bind(Server=self)
        BoundLogger.debug("Index web API request.")

        Out = ""
        Out += "<H1>Hello!</H1>"
        Out += "<H3>Endpoints:</H3>"
        Out += "<ol>"
        for View in self.Views:
            Out += "<li>" + View.__name__ + "</li>"
        Out += "</ol>"
        return Out

    def IsActive(self):
        """IsActive API endpoint."""
        BoundLogger = logger.bind(Server=self)
        BoundLogger.debug("IsActive web API request.")
        return dict(Response="Running")

    def Kill(self):
        """Kill API endpoint. Used to kill the server remotely."""
        BoundLogger = logger.bind(Server=self)
        BoundLogger.debug("Kill web API request.")

        ServerBackendABC.StopBackend(self)

        return dict(Response="Killed")
