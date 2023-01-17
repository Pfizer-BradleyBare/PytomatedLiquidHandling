import web

from ....Server.Globals.HandlerRegistry import GetAppHandler
from ....Server.Tools.Parser import Parser
from ...Workbook import WorkbookTracker

urls = (
    "/App/GetWorkbookContainers",
    "ABN.Source.App.Handler.Endpoints.GetWorkbookContainers.GetWorkbookContainers",
)


class GetWorkbookContainers:
    def POST(self):
        ParserObject = Parser("App GetWorkbookContainers", web.data())

        if not ParserObject.IsValid(["Workbook Name"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodName = ParserObject.GetEndpointInputData()["Workbook Name"]

        WorkbookTrackerInstance: WorkbookTracker = (
            GetAppHandler().WorkbookTrackerInstance  # type:ignore
        )

        WorkbookInstance = WorkbookTrackerInstance.GetObjectByName(MethodName)

        LabwareSelectionInstances = sorted(
            [
                LabwareSelectionInstance
                for LabwareSelectionInstance in WorkbookInstance.LabwareSelectionTrackerInstance.GetObjectsAsList()
            ],
            key=lambda LabwareSelectionInstance: LabwareSelectionInstance.GetName(),
        )

        ContainerNames = [
            LabwareSelectionInstance.GetContainer().GetName()
            for LabwareSelectionInstance in LabwareSelectionInstances
        ]

        LabwareNames = [
            LabwareSelectionInstance.GetContainer().GetName()
            for LabwareSelectionInstance in LabwareSelectionInstances
        ]

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
