import web

from PytomatedLiquidHandling.Server.Tools.Parser import Parser

urls = (
    "/App/GetWorkbookContainers",
    "App.Handler.Endpoints.GetWorkbookContainers.GetWorkbookContainers",
)


class GetWorkbookContainers:
    def POST(self):
        ParserObject = Parser("App GetWorkbookContainers", web.data())

        from ..Handler import GetHandler

        if not ParserObject.IsValid(["Workbook Name"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodName = ParserObject.GetEndpointInputData()["Workbook Name"]

        WorkbookTrackerInstance = GetHandler().WorkbookTrackerInstance

        WorkbookInstance = WorkbookTrackerInstance.GetObjectByName(MethodName)

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
