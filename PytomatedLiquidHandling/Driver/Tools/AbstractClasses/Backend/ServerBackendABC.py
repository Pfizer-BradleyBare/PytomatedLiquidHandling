import json
from threading import Event, Thread
from typing import Callable

from flask import Flask

from .....Tools.Logger import Logger
from .BackendABC import BackendABC


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
        Host = (self.Address, self.Port, self.PathPrefix)
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
        Host = (self.Address, self.Port, self.PathPrefix)
        if Host not in ServerBackendABC.__Hosts:
            raise Exception("This backend not currently running. Run it first")

        self.__AppParentThreadRunnerFlag.set()

        ServerBackendABC.__Hosts.remove(Host)

    def Kill(self):
        self.StopBackend()
        return "App killed for server with ID: " + str(self.GetUniqueIdentifier())

    class Parser:
        def __init__(
            self,
            LoggerInstance: Logger,
            EndpointID: str,
            JSONstring: bytes | None = None,
        ):
            LoggerInstance.debug("PARSER: __START__")
            LoggerInstance.info("PARSER: Handling Endpoint: %s", EndpointID)
            LoggerInstance.debug(
                "PARSER: Created Parser class with data: %s", str(JSONstring)
            )

            self.LoggerInstance: Logger = LoggerInstance
            self.EndpointID: str = EndpointID
            self.InputString: bytes | None = JSONstring
            self.JSON: dict | None = dict()
            self.EndpointState: bool = False
            self.EndpointMessage: str = "N/A"
            self.EndpointReturn: dict = dict()

            if not (JSONstring is None or JSONstring == "" or JSONstring == b""):
                try:
                    self.JSON = json.loads(JSONstring.decode().replace("'", ""))
                    LoggerInstance.debug(
                        "Request Data: \n%s",
                        json.dumps(self.JSON, indent=4, sort_keys=True),
                    )
                except Exception:
                    LoggerInstance.error("PARSER: Error Parsing Data! Bad format.")
                    self.JSON = None

        def __del__(self):

            self.LoggerInstance.debug("PARSER: __END__")

        def IsValid(self, ExpectedKeys: list[str]) -> bool:
            if self.JSON is None:
                self.EndpointMessage = (
                    "JSON Object could not be loaded correctly. Try again."
                )
                return False

            InputKeys = self.JSON.keys()

            # if len(InputKeys) != len(ExpectedKeys):
            #    self.EndpointMessage = (
            #        "Incorrect number of keys. This endpoint expects "
            #        + str(len(ExpectedKeys))
            #        + " keys. Expected: "
            #        + str(ExpectedKeys)
            #    )
            #    return False
            # Maybe extra keys doesn't matter?

            if not all(Key in InputKeys for Key in ExpectedKeys):
                self.EndpointMessage = (
                    "Incorrect keys given to input. Received: "
                    + str(InputKeys)
                    + " Expected: "
                    + str(ExpectedKeys)
                )
                return False

            return True

        def GetEndpointInputData(self, Key: str) -> any:  # type: ignore
            if self.JSON is None:
                return None

            return self.JSON[Key]

        def SetEndpointState(self, State: bool):
            self.EndpointState = State

        def SetEndpointMessage(self, Message: str):
            self.EndpointMessage = Message

        def SetEndpointOutputKey(self, Key: str, Value: any):  # type: ignore
            self.EndpointReturn[Key] = Value

        def GetHTTPResponse(self) -> str:

            Out = dict()
            Out["Endpoint ID"] = self.EndpointID
            Out["Endpoint State"] = self.EndpointState
            Out["Endpoint Message"] = self.EndpointMessage
            Out["Endpoint Input Data"] = self.JSON
            Out["Endpoint Output Data"] = self.EndpointReturn

            self.LoggerInstance.debug(
                "Response Data: \n%s", json.dumps(Out, indent=4, sort_keys=True)
            )
            return json.dumps(Out)