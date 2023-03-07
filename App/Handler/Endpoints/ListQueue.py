import web

from PytomatedLiquidHandling.Server.Tools.Parser import Parser

from ...Workbook import WorkbookRunTypes

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
                if Workbook.WorkbookRunType == WorkbookRunTypes.Run
            ]
        )

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey("Queued Workbooks", QueuedWorkbookNames)

        Response = ParserObject.GetHTTPResponse()
        return Response
