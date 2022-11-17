import web
import xlwings

from ..Tools.Parser import Parser

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

        if xlwings.apps.count != 0:
            for Book in xlwings.books:
                if Book.fullname == MethodFilePath:
                    Book.save()
                    App = Book.app
                    Book.close()
                    if len(App.books) == 0:
                        App.quit()

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Excel Workbook Closed")

        Response = ParserObject.GetHTTPResponse()
        return Response
