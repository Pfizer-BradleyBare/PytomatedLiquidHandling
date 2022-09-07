# curl -H "Content-Type: application/json" -X POST -d "{\"Method Path\":\"C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\_Template_MAM.xlsm\"}" http://localhost:65535/Method/Queue

import web
from ..Parser import Parser
import os
from ...Server import ServerVariables
from ...API.Workbook import WorkbookLoader

urls = ("/Method/Queue", "ABN.Source.Server.Method.Queue.Queue")


class Queue:
    def POST(self):
        ParserObject = Parser("Method Queue", web.data())

        if not ParserObject.IsValid():
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodPath = ParserObject.GetAPIData()["Method Path"]

        if ".xlsm" not in MethodPath:
            ParserObject.SetAPIReturn(
                {
                    "Reason": "Method Path is not an xlsm file. (Macro Enabled Excel File)"
                }
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        if not (os.access(MethodPath, os.F_OK) and os.access(MethodPath, os.W_OK)):
            ParserObject.SetAPIReturn(
                {"Reason": "Method Path does not exist or is read only"}
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is valid file path?

        WorkbookTrackerInstance = ServerVariables.WorkbookTrackerInstance

        PathsList = [
            Workbook.GetPath()
            for Workbook in WorkbookTrackerInstance.GetObjectsAsList()
        ]
        if MethodPath in PathsList:
            ParserObject.SetAPIReturn({"Reason": "Method is already running"})
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is workbook already running?

        WorkbookLoader.Load(ServerVariables.WorkbookTrackerInstance, MethodPath)
        # Do something here

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
