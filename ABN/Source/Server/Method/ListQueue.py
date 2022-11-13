import web
from ..Tools.Parser import Parser
from ..Globals.WorkbookTrackerInstance import WorkbookTrackerInstance
from ...API.Workbook import WorkbookRunTypes

urls = (
    "/Method/ListQueue",
    "ABN.Source.Server.Method.ListQueue.ListQueue",
)


class ListQueue:
    def GET(self):
        ParserObject = Parser("Method ListQueue", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

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

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn(
            "Message", "Returned queued methods and queued method information"
        )
        ParserObject.SetAPIReturn("Workbooks", RunningWorkbookNames)
        ParserObject.SetAPIReturn("Workbook Information", WorkbookInformation)

        Response = ParserObject.GetHTTPResponse()
        return Response
