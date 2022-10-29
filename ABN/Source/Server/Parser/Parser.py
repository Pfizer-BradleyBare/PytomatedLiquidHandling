import json
from ..Tools import LOG


class Parser:
    def __init__(self, APICallID: str, JSONstring: bytes | None = None):

        LOG.debug("PARSER: __START__")
        LOG.info("PARSER: Handling API: %s", APICallID)
        LOG.debug("PARSER: Created Parser class with data: %s", str(JSONstring))

        self.APICallID: str = APICallID
        self.string: bytes | None = JSONstring
        self.JSON: dict = dict()
        self.APIState: bool = False
        self.APIReturn: dict = dict()

        if not (JSONstring is None or JSONstring == "" or JSONstring == b""):
            try:
                self.JSON = json.loads(JSONstring.decode().replace("'", ""))
            except Exception:
                LOG.error("PARSER: Error Parsing Data! Bad format.")

        LOG.debug("Request Data: \n%s", json.dumps(self.JSON, indent=4, sort_keys=True))

    def __del__(self):
        LOG.debug("PARSER: __END__")

    def IsValid(self) -> bool:
        return self.JSON is not None

    def GetAPIData(self):
        return self.JSON

    def SetAPIState(self, State: bool):
        self.APIState = State

    def SetAPIReturn(self, Return: dict):
        self.APIReturn = Return

    def GetHTTPResponse(self) -> str:
        Out = dict()
        Out["APICallID"] = self.APICallID
        Out["APISuccess"] = self.APIState
        Out["APIData"] = self.JSON
        Out["APIReturn"] = self.APIReturn

        LOG.debug("Response Data: \n%s", json.dumps(Out, indent=4, sort_keys=True))
        return json.dumps(Out)
