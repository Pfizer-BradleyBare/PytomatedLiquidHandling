import web
from ..Tools.Parser import Parser
from ...Tools import Excel, ExcelOperator


urls = (
    "/Method/Close",
    "ABN.Source.Server.Method.Close.Close",
)


class Close:
    def POST(self):
        ParserObject = Parser("Method Close", web.data())

        if not ParserObject.IsValid(["Method File Path"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFilePath = ParserObject.GetAPIData()["Method File Path"]

        with ExcelOperator(False, Excel(MethodFilePath)) as ExcelOperatorInstance:
            ExcelOperatorInstance  # type: ignore
        # This will check if the book is already open and if so will close it.

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Excel Workbook Closed")

        Response = ParserObject.GetHTTPResponse()
        return Response
