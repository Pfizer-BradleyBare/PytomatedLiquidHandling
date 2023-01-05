import web

from ....Server.Globals.HandlerRegistry import GetAppHandler
from ....Server.Tools.Parser import Parser
from ...Workbook import WorkbookRunTypes, WorkbookTracker

urls = (
    "/App/ListQueue",
    "ABN.Source.App.Handler.Endpoints.ListQueue.ListQueue",
)


class ListQueue:
    def GET(self):
        ParserObject = Parser("App ListQueue", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        WorkbookTrackerInstance: WorkbookTracker = (
            GetAppHandler().WorkbookTrackerInstance  # type:ignore
        )

        QueuedWorkbookNames = sorted(
            [
                Workbook.GetName()
                for Workbook in WorkbookTrackerInstance.GetObjectsAsList()
                if Workbook.GetRunType() == WorkbookRunTypes.Run
                or Workbook.GetRunType() == WorkbookRunTypes.PreRun
            ]
        )

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey("Queued Workbooks", QueuedWorkbookNames)

        Response = ParserObject.GetHTTPResponse()
        return Response
