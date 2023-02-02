import json

from .... import Globals


class Parser:
    def __init__(self, EndpointID: str, JSONstring: bytes | None = None):

        LoggerInstance = Globals.GetLogger()

        LoggerInstance.debug("PARSER: __START__")
        LoggerInstance.info("PARSER: Handling Endpoint: %s", EndpointID)
        LoggerInstance.debug(
            "PARSER: Created Parser class with data: %s", str(JSONstring)
        )

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
        LoggerInstance = Globals.GetLogger()

        LoggerInstance.debug("PARSER: __END__")

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

    def GetEndpointInputData(self) -> dict:
        return self.JSON  # type: ignore

    def SetEndpointState(self, State: bool):
        self.EndpointState = State

    def SetEndpointMessage(self, Message: str):
        self.EndpointMessage = Message

    def SetEndpointOutputKey(self, Key: str, Value: any):  # type: ignore
        self.EndpointReturn[Key] = Value

    def GetHTTPResponse(self) -> str:
        LoggerInstance = Globals.GetLogger()

        Out = dict()
        Out["Endpoint ID"] = self.EndpointID
        Out["Endpoint State"] = self.EndpointState
        Out["Endpoint Message"] = self.EndpointMessage
        Out["Endpoint Input Data"] = self.JSON
        Out["Endpoint Output Data"] = self.EndpointReturn

        LoggerInstance.debug(
            "Response Data: \n%s", json.dumps(Out, indent=4, sort_keys=True)
        )
        return json.dumps(Out)
