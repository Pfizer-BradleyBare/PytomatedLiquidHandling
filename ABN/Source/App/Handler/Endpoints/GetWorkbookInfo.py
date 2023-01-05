import web

from ....Server.Globals.HandlerRegistry import GetAppHandler
from ....Server.Tools.Parser import Parser
from ...Workbook import WorkbookRunTypes, WorkbookTracker

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
            "4176641172",
            "BradleyBare@gmail.com",
            "Bradley.Bare@pfizer.com",
        ]
        # Get contact info

        Operations = ["Notify Owner"]

        Operations += ["Show Pending Notifications"]
        # Have any notifications fired?
        # Shared Operations

        if WorkbookInstance.GetRunType() == WorkbookRunTypes.PreRun:
            Operations += ["Dequeue"]

        else:  # Run
            Operations += [
                "Show Pathway States",
                "Deck Loading / Unloading",
                "Open Method",
                # "Repeat Step",
                "Pause",
                "Abort",
                "Dequeue",
            ]

        # Possible operations

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey(
            "Run Type", WorkbookInstance.GetRunType().value
        )
        ParserObject.SetEndpointOutputKey("Full Path", WorkbookInstance.GetPath())
        ParserObject.SetEndpointOutputKey("Owner", Owner)
        ParserObject.SetEndpointOutputKey("Contact Info", ", ".join(ContactInfo))
        ParserObject.SetEndpointOutputKey("Available Operations", Operations)

        Response = ParserObject.GetHTTPResponse()
        return Response
