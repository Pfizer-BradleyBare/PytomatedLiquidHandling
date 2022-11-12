import web
from ..Tools.Parser import Parser
import xlwings
from ...Tools import Excel, ExcelOperator


urls = (
    "/Method/Open",
    "ABN.Source.Server.Method.Open.Open",
)


class Open:
    def POST(self):
        ParserObject = Parser("Method Open", web.data())

        if not ParserObject.IsValid(["Method File Path"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFilePath = ParserObject.GetAPIData()["Method File Path"]

        with ExcelOperator(False, Excel(MethodFilePath)) as ExcelOperatorInstance:
            ExcelOperatorInstance  # type: ignore
        # This will check if the book is already open then close it.

        xlwings.Book(MethodFilePath)
        # Now we will open it no strings attached.

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Excel Workbook Opened")

        Response = ParserObject.GetHTTPResponse()
        return Response
