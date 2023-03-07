import web

from PytomatedLiquidHandling.Server.Tools.Parser import Parser

urls = (
    "/App/GetPathwayStates",
    "App.Handler.Endpoints.GetPathwayStates.GetPathwayStates",
)


class GetPathwayStates:
    def POST(self):
        ParserObject = Parser("App GetPathwayStates", web.data())

        from ..Handler import GetHandler

        if not ParserObject.IsValid(["Workbook Name"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodName = ParserObject.GetEndpointInputData()["Workbook Name"]

        WorkbookTrackerInstance = GetHandler().WorkbookTrackerInstance

        WorkbookInstance = WorkbookTrackerInstance.GetObjectByName(MethodName)

        ContextInstances = sorted(
            [
                ContextInstance
                for ContextInstance in WorkbookInstance.ContextTrackerInstance.GetObjectsAsList()
            ],
            key=lambda ContextInstance: ContextInstance.GetName(),
        )

        Contexts = [
            ContextInstance.GetName().replace(":__StartingContext__:", "")
            for ContextInstance in ContextInstances
        ]
        States = [
            ContextInstance.ContextStateInstance.State.value
            for ContextInstance in ContextInstances
        ]
        Reasons = [
            ContextInstance.ContextStateInstance.Reason
            for ContextInstance in ContextInstances
        ]
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
