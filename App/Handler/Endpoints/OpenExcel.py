import web

from PytomatedLiquidHandling.Server.Tools.Parser import Parser

from ...Tools import Excel

urls = (
    "/App/OpenExcel",
    "App.Handler.Endpoints.OpenExcel.OpenExcel",
)


class OpenExcel:
    def POST(self):
        ParserObject = Parser("App OpenExcel", web.data())

        if not ParserObject.IsValid(["Method File Path"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFilePath = ParserObject.GetEndpointInputData()["Method File Path"]

        ExcelInstance = Excel.Excel(MethodFilePath)
        ExcelInstance.OpenBook(True)

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
