from ..Tools.Parsing import ParseHTTPResponse

urls = ("/Comm/GetCommand", "ABN.Source.Server.Comm.GetCommand.GetCommand")


class GetCommand:
    def GET(self):
        print("GetCommand request received!")
        print("Method at top of queue will produce next command...")
        return ParseHTTPResponse({"Out": "Test"})
