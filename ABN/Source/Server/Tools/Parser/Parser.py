import json

from ...Globals import LOG


class Parser:
    def __init__(self, APICallID: str, JSONstring: bytes | None = None):

        LOG.debug("PARSER: __START__")
        LOG.info("PARSER: Handling API: %s", APICallID)
        LOG.debug("PARSER: Created Parser class with data: %s", str(JSONstring))

        self.APICallID: str = APICallID
        self.string: bytes | None = JSONstring
        self.JSON: dict | None = dict()
        self.APIState: bool = False
        self.APIReturn: dict = {"Message": ""}

        if not (JSONstring is None or JSONstring == "" or JSONstring == b""):
            try:
                self.JSON = json.loads(JSONstring.decode().replace("'", ""))
                LOG.debug(
                    "Request Data: \n%s",
                    json.dumps(self.JSON, indent=4, sort_keys=True),
                )
            except Exception:
                LOG.error("PARSER: Error Parsing Data! Bad format.")
                self.JSON = None

    def __del__(self):
        LOG.debug("PARSER: __END__")

    def IsValid(self, ExpectedKeys: list[str]) -> bool:
        if self.JSON is None:
            self.APIReturn[
                "Message"
            ] = "JSON Object could not be loaded correctly. Try again."
            return False

        InputKeys = self.JSON.keys()

        # if len(InputKeys) != len(ExpectedKeys):
        #    self.APIReturn["Message"] = (
        #        "Incorrect number of keys. This endpoint expects "
        #        + str(len(ExpectedKeys))
        #        + " keys. Expected: "
        #        + str(ExpectedKeys)
        #    )
        #    return False
        # Maybe extra keys doesn't matter?

        if not all(Key in InputKeys for Key in ExpectedKeys):
            self.APIReturn["Message"] = (
                "Incorrect keys given to input. Received: "
                + str(InputKeys)
                + " Expected: "
                + str(ExpectedKeys)
            )
            return False

        return True

    def GetAPIData(self) -> dict:
        return self.JSON  # type: ignore

    def SetAPIState(self, State: bool):
        self.APIState = State

    def SetAPIReturn(self, Key: str, Value: any):  # type: ignore
        self.APIReturn[Key] = Value

    def GetHTTPResponse(self) -> str:
        if self.APIReturn["Message"] == "":
            raise Exception("APIReturn Message key must be set. ALWAYS!")

        Out = dict()
        Out["APICallID"] = self.APICallID
        Out["APISuccess"] = self.APIState
        Out["APIData"] = self.JSON
        Out["APIReturn"] = self.APIReturn

        LOG.debug("Response Data: \n%s", json.dumps(Out, indent=4, sort_keys=True))
        return json.dumps(Out)
