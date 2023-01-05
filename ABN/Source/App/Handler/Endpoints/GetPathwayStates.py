import web

from ....Server.Globals.HandlerRegistry import GetAppHandler
from ....Server.Tools.Parser import Parser
from ...Workbook import WorkbookTracker

urls = (
    "/App/GetPathwayStates",
    "ABN.Source.App.Handler.Endpoints.GetPathwayStates.GetPathwayStates",
)


class GetPathwayStates:
    def POST(self):
        ParserObject = Parser("App GetPathwayStates", web.data())

        if not ParserObject.IsValid(["Workbook Name"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodName = ParserObject.GetEndpointInputData()["Workbook Name"]

        WorkbookTrackerInstance: WorkbookTracker = (
            GetAppHandler().WorkbookTrackerInstance  # type:ignore
        )

        WorkbookInstance = WorkbookTrackerInstance.GetObjectByName(MethodName)

        ContextInstances = sorted(
            [
                ContextInstance
                for ContextInstance in WorkbookInstance.GetActiveContextTracker().GetObjectsAsList()
                + WorkbookInstance.GetInactiveContextTracker().GetObjectsAsList()
            ],
            key=lambda ContextInstance: ContextInstance.GetName(),
        )

        Contexts = [
            ContextInstance.GetName().replace(":__StartingContext__:", "")
            for ContextInstance in ContextInstances
        ]
        States = [ContextInstance.State.State for ContextInstance in ContextInstances]
        Reasons = [ContextInstance.State.Reason for ContextInstance in ContextInstances]
        PathwayNames = [
            "Pathway " + str(Index) for Index in range(1, len(Contexts) + 1)
        ]

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey("Pathway Names", PathwayNames)
        ParserObject.SetEndpointOutputKey("Contexts", Contexts)
        ParserObject.SetEndpointOutputKey("States", States)
        ParserObject.SetEndpointOutputKey("Reasons", Reasons)

        Response = ParserObject.GetHTTPResponse()
        return Response
