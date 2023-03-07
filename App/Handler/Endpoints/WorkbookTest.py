# curl -X GET http://localhost:255/WorkbookTest

import os

import web

from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes
from PytomatedLiquidHandling.Server.Tools.Parser import Parser

from ...Workbook import WorkbookLoader, WorkbookRunTypes

urls = ("/WorkbookTest", "App.Handler.Endpoints.WorkbookTest.WorkbookTest")


class WorkbookTest:
    def GET(self):
        ParserObject = Parser("App WorkbookTest", web.data())

        from ..Handler import GetHandler

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        WorkbookTrackerInstance = GetHandler().WorkbookTrackerInstance

        MethodPath = "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\App\\_Template_MAM.xlsm"
        Action = WorkbookRunTypes("Run")
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
            Workbook.MethodPath
            for Workbook in WorkbookTrackerInstance.GetObjectsAsList()
        ]
        if MethodPath in PathsList:
            ParserObject.SetEndpointMessage("Method is already running")
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Is workbook already running?

        WorkbookLoader.Load(WorkbookTrackerInstance, MethodPath, Action)
        # Load the workbook path into the tracker

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
