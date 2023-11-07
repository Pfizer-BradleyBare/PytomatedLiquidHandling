import json
import logging
import time
from threading import Event, Thread
from typing import Any, Callable, ClassVar

from flask import Flask
from pydantic import PrivateAttr

from .SimpleBackendABC import SimpleBackendABC

ParserLogger = logging.getLogger(__name__ + ".Parser")


class ServerBackendABC(SimpleBackendABC):
    __Hosts: ClassVar[list[tuple]] = list()

    Views: list[Callable]
    PathPrefix: str = "/"
    Address: str = "localhost"
    Port: int = 8080
    _App: Flask = PrivateAttr()
    _AppParentThreadRunnerFlag: Event = PrivateAttr(default=Event())

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        self.__App = Flask(str(self.Identifier))
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
            name="Flask App Thread-> " + str(self.Identifier),
            target=self.__Run,
            daemon=True,
        ).start()

        self._AppParentThreadRunnerFlag.wait()
        time.sleep(1)

    def __Run(self):
        self.__App.run(self.Address, self.Port)

    def GetEndpointID(self, Endpoint: str):
        return self.__class__.__name__ + ": " + str(self.Identifier) + "-> " + Endpoint

    def StartBackend(self):
        SimpleBackendABC.StartBackend(self)
        Host = (self.Address, self.Port)
        if Host in ServerBackendABC.__Hosts:
            raise Exception(
                "This host is already taken. Choose a different address and/or port."
            )

        ServerBackendABC.__Hosts.append(Host)

        self._AppParentThreadRunnerFlag.clear()

        Thread(
            name="Flask App Thread Runner-> " + str(self.Identifier),
            target=self.__ServerThreadRunner,
        ).start()

    def StopBackend(self):
        SimpleBackendABC.StopBackend(self)
        Host = (self.Address, self.Port)
        if Host not in ServerBackendABC.__Hosts:
            raise Exception("This backend not currently running. Run it first")

        self._AppParentThreadRunnerFlag.set()

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
            self.GetEndpointID("IsActive"),
            None,
        )
        ParserInstance.SetEndpointState(True)
        ParserInstance.SetEndpointDetails("Backend is Active")
        return ParserInstance.GetHTTPResponse()

    def Kill(self):
        ServerBackendABC.StopBackend(self)
        ParserInstance = ServerBackendABC.Parser(
            self.GetEndpointID("Kill"),
            None,
        )
        ParserInstance.SetEndpointState(True)
        ParserInstance.SetEndpointDetails("Backend Killed")
        return ParserInstance.GetHTTPResponse()

    class Parser:
        def __init__(
            self,
            EndpointID: str,
            JSONstring: bytes | None = None,
        ):
            ParserLogger.debug("PARSER: __START__")
            ParserLogger.info("PARSER: Handling Endpoint: %s", EndpointID)
            ParserLogger.debug(
                "PARSER: Created Parser class with data: %s", str(JSONstring)
            )

            self.EndpointID: str = EndpointID
            self.InputString: bytes | None = JSONstring
            self.JSON: dict = {}
            self.EndpointState: bool = False
            self.EndpointDetails: str = "N/A"
            self.EndpointReturn: dict = dict()

            if not (JSONstring is None or JSONstring == "" or JSONstring == b""):
                try:
                    self.JSON = json.loads(JSONstring.decode().replace("'", ""))
                    ParserLogger.debug(
                        "Request Data: \n%s",
                        json.dumps(self.JSON, indent=4, sort_keys=True),
                    )
                except Exception:
                    ParserLogger.error("PARSER: Error Parsing Data! Bad format.")
                    self.JSON = {}

        def __del__(self):
            ParserLogger.debug("PARSER: __END__")

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

            ParserLogger.debug(
                "Response Data: \n%s", json.dumps(Out, indent=4, sort_keys=True)
            )
            return json.dumps(Out)
