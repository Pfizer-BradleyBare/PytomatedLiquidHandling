import json
import logging
import time
from dataclasses import dataclass, field
from threading import Event, Thread
from typing import Callable, ClassVar

from flask import Flask

from PytomatedLiquidHandling.Tools import Logger

from .SimpleBackendABC import SimpleBackendABC


@dataclass()
class ServerBackendABC(SimpleBackendABC):
    __Hosts: ClassVar[list[tuple]] = list()

    Views: list[Callable]
    PathPrefix: str = "/"
    Address: str = "localhost"
    Port: int = 8080
    __App: Flask = field(init=False)
    __AppParentThreadRunnerFlag: Event = field(init=False, default=Event())

    def __post_init__(self):
        self.__App = Flask(str(self.UniqueIdentifier))
        logging.getLogger("werkzeug").disabled = True
        self.Views += [self.IsActive, self.Kill]

        self.__App.add_url_rule(self.PathPrefix, "Index", self.Index)
        for View in self.Views:
            self.__App.add_url_rule(
                self.PathPrefix + View.__name__,
                View.__name__,
                View,
                methods=["GET", "POST"],
            )

    def __ServerThreadRunner(self):
        Thread(
            name="Flask App Thread-> " + str(self.UniqueIdentifier),
            target=self.__Run,
            daemon=True,
        ).start()

        self.__AppParentThreadRunnerFlag.wait()
        time.sleep(1)

    def __Run(self):
        self.__App.run(self.Address, self.Port)

    def GetEndpointID(self, Endpoint: str):
        return (
            self.__class__.__name__
            + ": "
            + str(self.UniqueIdentifier)
            + "-> "
            + Endpoint
        )

    def StartBackend(self):
        SimpleBackendABC.StartBackend(self)
        Host = (self.Address, self.Port)
        if Host in ServerBackendABC.__Hosts:
            raise Exception(
                "This host is already taken. Choose a different address and/or port."
            )

        ServerBackendABC.__Hosts.append(Host)

        self.__AppParentThreadRunnerFlag.clear()

        Thread(
            name="Flask App Thread Runner-> " + str(self.UniqueIdentifier),
            target=self.__ServerThreadRunner,
        ).start()

    def StopBackend(self):
        SimpleBackendABC.StopBackend(self)
        Host = (self.Address, self.Port)
        if Host not in ServerBackendABC.__Hosts:
            raise Exception("This backend not currently running. Run it first")

        self.__AppParentThreadRunnerFlag.set()

        ServerBackendABC.__Hosts.remove(Host)

    def Index(self):
        Out = ""
        Out += "<H1>Hello!</H1>"
        Out += "<H3>Endpoints:</H3>"
        Out += "<ol>"
        for View in self.Views:
            Out += "<li>" + View.__name__ + "</li>"
        Out += "</ol>"
        return Out

    def IsActive(self):
        ParserInstance = ServerBackendABC.Parser(
            self.LoggerInstance,
            self.GetEndpointID("IsActive"),
            None,
        )
        ParserInstance.SetEndpointState(True)
        ParserInstance.SetEndpointDetails("Backend is Active")
        return ParserInstance.GetHTTPResponse()

    def Kill(self):
        ServerBackendABC.StopBackend(self)
        ParserInstance = ServerBackendABC.Parser(
            self.LoggerInstance,
            self.GetEndpointID("Kill"),
            None,
        )
        ParserInstance.SetEndpointState(True)
        ParserInstance.SetEndpointDetails("Backend Killed")
        return ParserInstance.GetHTTPResponse()

    @dataclass
    class Parser:
        def __init__(
            self,
            LoggerInstance: Logger.Logger,
            EndpointID: str,
            JSONstring: bytes | None = None,
        ):
            LoggerInstance.debug("PARSER: __START__")
            LoggerInstance.info("PARSER: Handling Endpoint: %s", EndpointID)
            LoggerInstance.debug(
                "PARSER: Created Parser class with data: %s", str(JSONstring)
            )

            self.LoggerInstance: Logger.Logger = LoggerInstance
            self.EndpointID: str = EndpointID
            self.InputString: bytes | None = JSONstring
            self.JSON: dict = {}
            self.EndpointState: bool = False
            self.EndpointDetails: str = "N/A"
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
                    self.JSON = {}

        def __del__(self):
            self.LoggerInstance.debug("PARSER: __END__")

        def IsValid(self, ExpectedKeys: list[str]) -> bool:
            if self.JSON == {}:
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
            if self.JSON == {}:
                return None

            return self.JSON[Key]

        def SetEndpointState(self, State: bool):
            self.EndpointState = State

        def SetEndpointDetails(self, Details: str):
            self.EndpointDetails = Details

        def SetEndpointOutputKey(self, Key: str, Value: any):  # type: ignore
            self.EndpointReturn[Key] = Value

        def GetHTTPResponse(self) -> str:
            Out = dict()
            Out["Endpoint ID"] = self.EndpointID
            Out["Endpoint State"] = self.EndpointState
            Out["Endpoint Details"] = self.EndpointDetails
            Out["Endpoint Input Data"] = self.JSON
            Out["Endpoint Output Data"] = self.EndpointReturn

            self.LoggerInstance.debug(
                "Response Data: \n%s", json.dumps(Out, indent=4, sort_keys=True)
            )
            return json.dumps(Out)
