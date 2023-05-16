from .BackendABC import BackendABC
from flask import Flask
from threading import Thread, Event
from typing import Callable
import json
from .....Tools.Logger import Logger


class ServerBackendABC(BackendABC):
    __Hosts: list[tuple] = list()

    def __init__(
        self,
        UniqueIdentifier: str,
        LoggerInstance: Logger,
        Views: list[Callable],
        PathPrefix: str = "/",
        Address: str = "localhost",
        Port: int = 8080,
    ):
        BackendABC.__init__(self, UniqueIdentifier, LoggerInstance)
        self.__App = Flask(UniqueIdentifier)
        self.__AppParentThreadRunnerFlag: Event = Event()

        self.PathPrefix: str = PathPrefix
        self.Address: str = Address
        self.Port: int = Port
        self.Views: list[Callable] = Views + [self.Kill]

        for View in self.Views:
            self.__App.add_url_rule(PathPrefix + View.__name__, View.__name__, View)

    def __ServerThreadRunner(self):
        Thread(
            name="Flask App Thread-> " + str(self.GetUniqueIdentifier()),
            target=self.__Run,
            daemon=True,
        ).start()

        self.__AppParentThreadRunnerFlag.wait()

    def __Run(self):
        self.__App.run(self.Address, self.Port)

    def StartBackend(self):
        Host = (self.Address, self.Port)
        if Host in ServerBackendABC.__Hosts:
            raise Exception(
                "This host is already taken. Choose a different address and/or port."
            )

        ServerBackendABC.__Hosts.append(Host)

        self.__AppParentThreadRunnerFlag.clear()

        Thread(
            name="Flask App Thread Runner-> " + str(self.GetUniqueIdentifier()),
            target=self.__ServerThreadRunner,
        ).start()

    def StopBackend(self):
        Host = (self.Address, self.Port)
        if Host not in ServerBackendABC.__Hosts:
            raise Exception("This backend not currently running. Run it first")

        self.__AppParentThreadRunnerFlag.set()

        ServerBackendABC.__Hosts.remove((self.Address, self.Port))

    def Kill(self):
        self.StopBackend()
        return "App killed for server with ID: " + str(self.GetUniqueIdentifier())
