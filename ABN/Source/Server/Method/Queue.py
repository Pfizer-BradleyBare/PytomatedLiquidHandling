# curl -H "Content-Type: application/json" -X POST -d "{\"Method Path\":\"C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\_Template_MAM.xlsm\",\"Requested Action\":\"Test\"}" http://localhost:65535/Method/Queue

import web
from ..Parser import Parser
import os
from ...Server.Globals.WorkbookTrackerInstance import WorkbookTrackerInstance
from ...API.Workbook import WorkbookLoader, WorkbookRunTypes

urls = ("/Method/Queue", "ABN.Source.Server.Method.Queue.Queue")


class Queue:
    def POST(self):
        ParserObject = Parser("Method Queue", web.data())

        if not ParserObject.IsValid():
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodPath = ParserObject.GetAPIData()["Method Path"]
        Action = ParserObject.GetAPIData()["Requested Action"]
        # acceptable values are "Test", "PrepList", or "Run"

        if ".xlsm" not in MethodPath:
            ParserObject.SetAPIReturn(
                {
                    "Reason": "Method Path is not an xlsm file. (Macro Enabled Excel File)"
                }
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is method actually there

        if not (os.access(MethodPath, os.F_OK) and os.access(MethodPath, os.W_OK)):
            ParserObject.SetAPIReturn(
                {"Reason": "Method Path does not exist or is read only"}
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is valid file path?

        PathsList = [
            Workbook.GetPath()
            for Workbook in WorkbookTrackerInstance.GetObjectsAsList()
        ]
        if MethodPath in PathsList:
            ParserObject.SetAPIReturn({"Reason": "Method is already running"})
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is workbook already running?

        WorkbookLoader.Load(WorkbookTrackerInstance, MethodPath, WorkbookRunTypes.Test)
        # Load the workbook path into the tracker

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
