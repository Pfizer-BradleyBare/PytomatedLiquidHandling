# curl -H "Content-Type: application/json" -X POST -d "{\"Method Path\":\"C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\_Template_MAM.xlsm\",\"Action\":\"Test\",\"User Name\":\"Test\",\"User Contact Info\":\"Test\"}" http://localhost:255/Method/Queue

# ##### API Definition #####
#
# Keys:
#   "Method Path"
#   "Action"
#
# ##########################


import os

import web

from ....Server.Globals.HandlerRegistry import GetAppHandler
from ....Server.Tools.Parser import Parser
from ...Workbook import WorkbookLoader, WorkbookRunTypes, WorkbookTracker

urls = ("/Method/Queue", "ABN.Source.App.Handler.Endpoints.Queue.Queue")


class Queue:
    def POST(self):
        ParserObject = Parser("App Queue", web.data())

        if not ParserObject.IsValid(
            ["Method Path", "Action", "User Name", "User Contact Info"]
        ):
            Response = ParserObject.GetHTTPResponse()
            return Response

        WorkbookTrackerInstance: WorkbookTracker = (
            GetAppHandler().WorkbookTrackerInstance  # type:ignore
        )

        MethodPath = ParserObject.GetEndpointInputData()["Method Path"]
        Action = WorkbookRunTypes(ParserObject.GetEndpointInputData()["Action"])
        # acceptable values are "Test", "PrepList", or "Run"

        if ".xlsm" not in MethodPath:
            ParserObject.SetEndpointMessage(
                "Method Path is not an xlsm file. (Macro Enabled Excel File)"
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is method actually there

        if not (os.access(MethodPath, os.F_OK) and os.access(MethodPath, os.W_OK)):
            ParserObject.SetEndpointMessage(
                "Method Path does not exist or is read only (User Error. Save Excel File?)",
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is valid file path?

        PathsList = [
            Workbook.GetPath()
            for Workbook in WorkbookTrackerInstance.GetObjectsAsList()
        ]
        if MethodPath in PathsList:
            ParserObject.SetEndpointMessage("Method is already running")
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is workbook already running?

        if Action == WorkbookRunTypes.Run:
            Action = WorkbookRunTypes.PreRun

        WorkbookLoader.Load(WorkbookTrackerInstance, MethodPath, Action)
        # Load the workbook path into the tracker

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
