import os

import web

from ....Server.Globals.HandlerRegistry import GetAppHandler
from ....Server.Tools.Parser import Parser
from ...Workbook import WorkbookTracker
from .AvailableMethods import MethodsPath, TempFolder

urls = (
    "/App/CleanupMethodProject",
    "ABN.Source.App.Handler.Endpoints.CleanupMethodProject.CleanupMethodProject",
)


class CleanupMethodProject:
    def POST(self):
        ParserObject = Parser("App CleanupMethodProject", web.data())

        if not ParserObject.IsValid(["Method", "Project"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        Method = ParserObject.GetEndpointInputData()["Method"]
        Project = ParserObject.GetEndpointInputData()["Project"]

        if Method == "Custom":
            ParserObject.SetEndpointState(True)
            ParserObject.SetEndpointMessage(
                "Nothing to clean. User loaded Custom Method"
            )

            Response = ParserObject.GetHTTPResponse()
            return Response

        CleanupPath = os.path.join(
            MethodsPath,
            Method,
            Project,
            TempFolder,
        )

        WorkbookTrackerInstance: WorkbookTracker = (
            GetAppHandler().WorkbookTrackerInstance  # type:ignore
        )

        QueuedFiles = [
            File.GetName() for File in WorkbookTrackerInstance.GetObjectsAsList()
        ]

        for File in os.listdir(CleanupPath):
            if File not in QueuedFiles:
                os.remove(os.path.join(CleanupPath, File))

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointMessage(
            Method + "-" + Project + "-" + TempFolder + " directory cleaned"
        )

        Response = ParserObject.GetHTTPResponse()
        return Response
