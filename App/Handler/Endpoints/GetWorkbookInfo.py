import web

from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes
from PytomatedLiquidHandling.Server.Tools.Parser import Parser

urls = (
    "/App/GetWorkbookInfo",
    "App.Handler.Endpoints.GetWorkbookInfo.GetWorkbookInfo",
)


class GetWorkbookInfo:
    def POST(self):
        ParserObject = Parser("App GetWorkbookInfo", web.data())

        from ..Handler import GetHandler

        if not ParserObject.IsValid(["Workbook Name"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodName = ParserObject.GetEndpointInputData()["Workbook Name"]

        WorkbookTrackerInstance = GetHandler().WorkbookTrackerInstance

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

        if WorkbookInstance.APIRunType == RunTypes.SimulatePartial:
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
            "Run Type", WorkbookInstance.WorkbookRunType.value
        )
        ParserObject.SetEndpointOutputKey("Full Path", WorkbookInstance.MethodPath)
        ParserObject.SetEndpointOutputKey("Owner", Owner)
        ParserObject.SetEndpointOutputKey("Contact Info", ", ".join(ContactInfo))
        ParserObject.SetEndpointOutputKey("Available Operations", Operations)

        Response = ParserObject.GetHTTPResponse()
        return Response
