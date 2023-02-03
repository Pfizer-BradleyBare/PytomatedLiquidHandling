import web

from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes
from PytomatedLiquidHandling.Server.Tools.Parser import Parser

urls = (
    "/App/ListQueue",
    "App.Handler.Endpoints.ListQueue.ListQueue",
)


class ListQueue:
    def GET(self):
        ParserObject = Parser("App ListQueue", web.data())

        from ..Handler import GetHandler

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        WorkbookTrackerInstance = GetHandler().WorkbookTrackerInstance

        QueuedWorkbookNames = sorted(
            [
                Workbook.GetName()
                for Workbook in WorkbookTrackerInstance.GetObjectsAsList()
                if Workbook.GetRunType() == RunTypes.Run
                or Workbook.GetRunType() == RunTypes.SimulateFull
            ]
        )

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey("Queued Workbooks", QueuedWorkbookNames)

        Response = ParserObject.GetHTTPResponse()
        return Response
