from __future__ import annotations

import logging
import time
from dataclasses import field
from threading import Event, Thread
from typing import Callable, ClassVar

from flask import Flask
from loguru import logger
from pydantic import dataclasses

from .backend_simple_base import BackendSimpleBase


@dataclasses.dataclass(kw_only=True)
class BackendServerBase(BackendSimpleBase):
    """Creates a web API for communication with the system software."""

    __hosts: ClassVar[list[tuple]] = []
    """Currently running web API hosts"""

    address: str = "localhost"
    """Web address to request web API endpoints."""

    port: int = 8080
    """Web port to request web API endpoints."""

    sub_domain: str = "/"
    """Web sub domain to request web API endpoints."""

    views: list[Callable]
    """Endpoints that the web API exposes."""

    _app: Flask = field(init=False)
    _app_parent_thread_runner_flag: Event = field(init=False)

    def __post_init__(self: BackendServerBase) -> None:
        """Creates the web API based on ```Address```, ```Port```, ```SubDomain```, and ```Views```."""
        self._app_parent_thread_runner_flag = Event()

        self._app = Flask(str(self.identifier))
        logging.getLogger("werkzeug").disabled = True

        self.views += [self.is_active, self.kill]
        self._app.add_url_rule(self.sub_domain, "Index", self.index)
        for view in self.views:
            self._app.add_url_rule(
                self.sub_domain + view.__name__,
                view.__name__,
                view,
                methods=["GET", "POST"],
            )

    def __server_thread_runner(self: BackendServerBase) -> None:
        Thread(
            name="Flask App Thread-> " + str(self.identifier),
            target=self.__run,
            daemon=True,
        ).start()

        self._app_parent_thread_runner_flag.wait()
        time.sleep(1)

    def __run(self: BackendServerBase) -> None:
        self._app.run(self.address, self.port)

    def _get_endpoint_id(self: BackendServerBase, endpoint: str) -> str:
        return f"{self.__class__.__name__}: {self.identifier}-> {endpoint}"

    def start(self: BackendServerBase) -> None:
        """- Checks that host is available. If host is not available then raises ```ValueError```.
        - Starts server as daemon thread."""
        BackendSimpleBase.start(self)
        host = (self.address, self.port)
        if host in BackendServerBase.__hosts:
            msg = "This host is already taken. Choose a different address and/or port."
            raise ValueError(msg)

        BackendServerBase.__hosts.append(host)

        self._app_parent_thread_runner_flag.clear()

        Thread(
            name=f"Flask App Thread Runner-> {self.identifier}",
            target=self.__server_thread_runner,
        ).start()

    def stop(self: BackendServerBase) -> None:
        """Kills server and all daemon threads. NOTE: expect 1 second delay. If server is not running then raises ```RuntimeError```."""
        BackendSimpleBase.stop(self)
        host = (self.address, self.port)
        if host not in BackendServerBase.__hosts:
            msg = "This backend not currently running. Run it first"
            raise RuntimeError(msg)

        self._app_parent_thread_runner_flag.set()

        BackendServerBase.__hosts.remove(host)

    def index(self: BackendServerBase):  # noqa: ANN201
        """Index API endpoint."""
        bound_logger = logger.bind(Server=self)
        bound_logger.debug("Index web API request.")

        response = ""
        response += "<H1>Hello!</H1>"
        response += "<H3>Endpoints:</H3>"
        response += "<ol>"
        for view in self.views:
            response += "<li>" + view.__name__ + "</li>"
        response += "</ol>"
        return response, 200

    def is_active(self: BackendServerBase) -> tuple:
        """IsActive API endpoint."""
        bound_logger = logger.bind(Server=self)
        bound_logger.debug("IsActive web API request.")
        return "Running", 200

    def kill(self: BackendServerBase) -> tuple:
        """Kill API endpoint. Used to kill the server remotely."""
        bound_logger = logger.bind(Server=self)
        bound_logger.debug("Kill web API request.")

        BackendServerBase.stop(self)

        return "Killed", 202
