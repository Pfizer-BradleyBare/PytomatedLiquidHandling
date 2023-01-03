import web

from ....Server.Globals.HandlerRegistry import GetAppHandler
from ....Server.Tools.Parser import Parser
from ...Workbook import WorkbookTracker

urls = (
    "/App/GetWorkbookInfo",
    "ABN.Source.App.Handler.Endpoints.GetWorkbookInfo.GetWorkbookInfo",
)


class GetWorkbookInfo:
    def POST(self):
        ParserObject = Parser("App GetWorkbookInfo", web.data())

        if not ParserObject.IsValid(["Workbook Name"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodName = ParserObject.GetEndpointInputData()["Workbook Name"]

        WorkbookTrackerInstance: WorkbookTracker = (
            GetAppHandler().WorkbookTrackerInstance  # type:ignore
        )

        WorkbookInstance = WorkbookTrackerInstance.GetObjectByName(MethodName)

        Owner = "STL and AND"
        ContactInfo = [
            "phone",
            "Phone2",
            "Email",
            "asdasdhvasbdakbdkjabdshbasdjbasbasbdajksbd",
            "asjkbdakjdsbakjsbdad",
        ]
        # Get contact info

        Operations = ["op1", "Op2", "op3"]
        # Possible operations

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey("Owner", Owner)
        ParserObject.SetEndpointOutputKey("Contact Info", ", ".join(ContactInfo))
        ParserObject.SetEndpointOutputKey("Available Operations", Operations)

        Response = ParserObject.GetHTTPResponse()
        return Response
