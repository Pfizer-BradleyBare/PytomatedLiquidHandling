import web

from ....Server.Tools.Parser import Parser
from ...Tools import Excel

urls = (
    "/App/CloseExcel",
    "ABN.Source.App.Handler.Endpoints.CloseExcel.CloseExcel",
)


class CloseExcel:
    def POST(self):
        ParserObject = Parser("App CloseExcel", web.data())

        if not ParserObject.IsValid(["Method File Path"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFilePath = ParserObject.GetEndpointInputData()["Method File Path"]

        ExcelInstance = Excel.Excel(MethodFilePath)
        ExcelInstance.OpenBook(True)
        ExcelInstance.CloseBook()

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
