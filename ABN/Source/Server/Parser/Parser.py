import json


class Parser:
    def __init__(self, APICallID: str, JSONstring: str = None):
        print()
        print("PARSER: __START__")
        print("PARSER: Handling API:", APICallID)
        print("PARSER: Created Parser class with data:", JSONstring)

        self.APICallID: str = APICallID
        self.string: str = JSONstring
        self.JSON: dict = dict()
        self.APIState: bool = False
        self.APIReturn: dict = dict()

        if not (JSONstring is None or JSONstring == "" or JSONstring == b""):
            try:
                self.JSON = json.loads(JSONstring.decode().replace("'", ""))
            except Exception:
                print("PARSER: Error Parsing Data! Bad format.")

        print("Request Data:", json.dumps(self.JSON, indent=4, sort_keys=True))

    def __del__(self):
        print("PARSER: __END__")
        print()

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

        print("Response Data:", json.dumps(Out, indent=4, sort_keys=True))
        return json.dumps(Out)
