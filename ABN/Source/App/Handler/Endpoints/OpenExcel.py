import web
import xlwings

from ....Server.Tools.Parser import Parser

urls = (
    "/App/OpenExcel",
    "ABN.Source.App.Handler.Endpoints.OpenExcel.OpenExcel",
)


class OpenExcel:
    def POST(self):
        ParserObject = Parser("App OpenExcel", web.data())

        if not ParserObject.IsValid(["Method File Path"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFilePath = ParserObject.GetEndpointInputData()["Method File Path"]

        BookHandle: xlwings.Book | None = None
        if xlwings.apps.count != 0:
            for Book in xlwings.books:
                if Book.fullname == MethodFilePath:
                    BookHandle = Book

        if BookHandle is None:
            BookHandle = xlwings.Book(MethodFilePath)

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
