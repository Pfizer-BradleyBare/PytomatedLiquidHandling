import web
import xlwings

from ....Server.Tools.Parser import Parser

urls = (
    "/Method/Close",
    "ABN.Source.App.Handler.Endpoints.Close.Close",
)


class Close:
    def POST(self):
        ParserObject = Parser("App Close", web.data())

        if not ParserObject.IsValid(["Method File Path"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFilePath = ParserObject.GetEndpointInputData()["Method File Path"]

        if xlwings.apps.count != 0:
            for Book in xlwings.books:
                if Book.fullname == MethodFilePath:
                    Book.save()
                    App = Book.app
                    Book.close()
                    if len(App.books) == 0:
                        App.quit()

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
