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

        RunningWorkbookNames = [
            Workbook.GetName()
            for Workbook in WorkbookTrackerInstance.GetObjectsAsList()
            if Workbook.GetRunType() == WorkbookRunTypes.Run
            or Workbook.GetRunType() == WorkbookRunTypes.PreRun
        ]

        WorkbookInformation = dict()

        for WorkbookName in RunningWorkbookNames:
            Workbook = WorkbookTrackerInstance.GetObjectByName(WorkbookName)
            WorkbookInformation[WorkbookName] = {"State": Workbook.GetState().value}

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointMessage(
            "Returned queued methods and queued method information"
        )
        ParserObject.SetEndpointOutputKey("Workbooks", RunningWorkbookNames)
        ParserObject.SetEndpointOutputKey("Workbook Information", WorkbookInformation)

        Response = ParserObject.GetHTTPResponse()
        return Response
