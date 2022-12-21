import os

import web

from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ....Server.Tools.Parser import Parser
from ...Workbook import WorkbookTracker
from .AvailableMethods import MethodsPath, TempFolder

urls = (
    "/Method/CleanupMethodProject",
    "ABN.Source.App.Handler.Endpoints.CleanupMethodProject.CleanupMethodProject",
)


class CleanupMethodProject:
    def POST(self):
        ParserObject = Parser("App CleanupMethodProject", web.data())

        if not ParserObject.IsValid(["Method", "Project"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        Method = ParserObject.GetAPIData()["Method"]
        Project = ParserObject.GetAPIData()["Project"]

        if Method == "Custom":
            ParserObject.SetAPIState(True)
            ParserObject.SetAPIReturn(
                "Message",
                "Nothing to clean. User loaded Custom Method",
            )

            Response = ParserObject.GetHTTPResponse()
            return Response

        CleanupPath = os.path.join(
            MethodsPath,
            Method,
            Project,
            TempFolder,
        )

        WorkbookTrackerInstance: WorkbookTracker = HandlerRegistry.GetObjectByName(
            "App"
        ).WorkbookTrackerInstance  # type:ignore

        QueuedFiles = [
            File.GetName() for File in WorkbookTrackerInstance.GetObjectsAsList()
        ]

        for File in os.listdir(CleanupPath):
            if File not in QueuedFiles:
                os.remove(os.path.join(CleanupPath, File))

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn(
            "Message", Method + "-" + Project + "-" + TempFolder + " directory cleaned"
        )

        Response = ParserObject.GetHTTPResponse()
        return Response
